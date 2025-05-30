from typing import Optional, List
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_postgres import PGVector
from pydantic import BaseModel
from langchain_core.documents import Document
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
import logging

from settings import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manage SQLAlchemy database connections and operations"""
    
    def __init__(self):
        self.connection_string = f"postgresql+psycopg://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
        self.engine = None
        self.SessionLocal = None
        self._setup_engine()
    
    def _setup_engine(self):
        """Setup SQLAlchemy engine with connection pooling"""
        self.engine = create_engine(
            self.connection_string,
            # Connection pooling configuration
            poolclass=QueuePool,
            pool_size=10,
            max_overflow=20,
            pool_pre_ping=True,  # Verify connections before use
            pool_recycle=3600,   # Recycle connections every hour
            # Additional options
            echo=False,  # Set to True for SQL debugging
            future=True  # Use SQLAlchemy 2.0 style
        )
        
        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine
        )
        
        logger.info("✅ SQLAlchemy engine configured successfully")
    
    def get_engine(self):
        """Get SQLAlchemy engine"""
        return self.engine
    
    def get_session(self):
        """Get SQLAlchemy session"""
        return self.SessionLocal()
    
    def setup_pgvector_extension(self):
        """Setup pgvector extension using SQLAlchemy"""
        try:
            with self.engine.connect() as conn:
                # Enable pgvector extension
                conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
                conn.commit()
                
                # Verify installation
                result = conn.execute(text(
                    "SELECT extname, extversion FROM pg_extension WHERE extname = 'vector';"
                )).fetchone()
                
                if result:
                    logger.info(f"✅ pgvector extension enabled - version: {result[1]}")
                    return True
                else:
                    logger.error("❌ pgvector extension not found")
                    return False
                    
        except Exception as e:
            logger.error(f"❌ Error setting up pgvector: {e}")
            return False
    
    def test_connection(self):
        """Test database connection"""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("SELECT version();")).fetchone()
                logger.info(f"✅ Database connection successful: {result[0][:50]}...")
                return True
        except Exception as e:
            logger.error(f"❌ Database connection failed: {e}")
            return False
    
    def get_connection_info(self):
        """Get connection pool information"""
        pool = self.engine.pool
        return {
            "pool_size": pool.size(),
            "checked_in": pool.checkedin(),
            "checked_out": pool.checkedout(),
            "overflow": pool.overflow()
        }
    
    def close(self):
        """Close all connections"""
        if self.engine:
            self.engine.dispose()
            logger.info("✅ Database connections closed")


class RAGCore:
    def __init__(self, db_manager: DatabaseManager, collection_name: str = "documents"):
        self.db_manager = db_manager
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small", api_key=settings.OPENAI_API_KEY, chunk_size=200)
        self.collection_name = collection_name
        self.vector_store = None

    def process_document_list(self, documents: List[List]) -> PGVector:
        """Process a list of documents where each document is [idx, knowledge_id, final_content]"""
        logger.info(f"Processing {len(documents)} documents...")
        
        processed_docs = []
        for doc in documents:
            if len(doc) != 3:
                logger.warning(f"Skipping invalid document format: {doc}")
                continue
                
            idx, knowledge_id, final_content = doc
            
            # Create document with metadata
            doc_with_metadata = Document(
                page_content=final_content,
                metadata={
                    "idx": str(idx),
                    "knowledge_id": str(knowledge_id)
                }
            )
            processed_docs.append(doc_with_metadata)
        
        # Create vector store using SQLAlchemy engine
        self.vector_store = PGVector.from_documents(
            documents=processed_docs,
            embedding=self.embeddings,
            connection=self.db_manager.get_engine(),  # Pass SQLAlchemy engine
            collection_name=self.collection_name,
            use_jsonb=True,
            pre_delete_collection=False
        )
        
        logger.info(f"✅ Created vector store with {len(processed_docs)} documents")
        return self.vector_store

    def get_vector_store(self):
        """Get the current vector store"""
        return self.vector_store

    def load_existing_vector_store(self) -> Optional[PGVector]:
        """Load an existing vector store from database"""
        try:
            self.vector_store = PGVector(
                embeddings=self.embeddings,
                connection=self.db_manager.get_engine(),  # Pass SQLAlchemy engine
                collection_name=self.collection_name,
                use_jsonb=True
            )
            logger.info(f"✅ Loaded existing vector store: {self.collection_name}")
            return self.vector_store
        except Exception as e:
            logger.error(f"❌ Error loading vector store: {e}")
            return None

    def get_collection_stats(self):
        """Get statistics about the collection using SQLAlchemy"""
        try:
            with self.db_manager.get_session() as session:
                # Query collection statistics
                query = text(f"""
                    SELECT 
                        COUNT(*) as total_documents,
                        COUNT(DISTINCT (cmetadata->>'knowledge_id')) as unique_knowledge_groups
                    FROM langchain_pg_embedding 
                    WHERE collection_id = (
                        SELECT uuid FROM langchain_pg_collection 
                        WHERE name = :collection_name
                    )
                """)
                
                result = session.execute(query, {"collection_name": self.collection_name}).fetchone()
                
                if result:
                    return {
                        "total_documents": result[0],
                        "unique_knowledge_groups": result[1],
                        "collection_name": self.collection_name
                    }
                else:
                    return {"total_documents": 0, "unique_knowledge_groups": 0}
                    
        except Exception as e:
            logger.error(f"❌ Error getting collection stats: {e}")
            return {"error": str(e)}


class RelevanceResponse(BaseModel):
    """Structure for relevance scoring response"""
    is_relevant: bool
    confidence: float
    explanation: str


class QueryEngine:
    def __init__(self, vector_store: Optional[PGVector] = None, initial_k: int = 10):
        self.vector_store = vector_store
        self.initial_k = initial_k
        
        # Create the relevance checking prompt
        self.relevance_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert at determining whether a article is relevant to a given question.
            Analyze the content carefully and determine if it contains information that would help answer the question.
            Consider both direct answers and contextually relevant information."""),
            ("user", """Question: {question}

Article:
[Index: {idx}]
{content}

Determine if this article is relevant to answering the question. Provide:
1. is_relevant: true/false
2. confidence: Score between 0 and 1
3. explanation: Brief explanation of your decision""")
        ])
        
        self.relevance_llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0,
            api_key=settings.OPENAI_API_KEY
        ).with_structured_output(RelevanceResponse)
        
    def set_vector_store(self, vector_store: PGVector):
        """Set the vector store to use for queries"""
        self.vector_store = vector_store

    def _deduplicate_docs(self, docs):
        """Deduplicate documents based on their index"""
        seen_indices = set()
        unique_docs = []
        
        for doc in docs:
            idx = doc.metadata.get("idx")
            if idx not in seen_indices:
                seen_indices.add(idx)
                unique_docs.append(doc)
        
        return unique_docs

    def _check_relevance(self, question: str, doc_content: str, idx: str):
        """Check if a document is relevant to the question using LLM"""
        try:
            response = self.relevance_llm.invoke(
                self.relevance_prompt.format(
                    question=question,
                    idx=idx,
                    content=doc_content
                )
            )
            logger.debug(f"Document {idx} - Relevant: {response.is_relevant}, Confidence: {response.confidence}")
            return response.is_relevant, response.confidence, response.explanation
        except Exception as e:
            logger.error(f"Error in relevance checking for document {idx}: {e}")
            return False, 0.0, str(e)

    def query(self, question: str, relevance_threshold: float = 0.85, filter=None):
        """Query the RAG system with LLM re-ranking"""
        if not self.vector_store:
            raise ValueError("Vector store not set. Please set a vector store before querying.")
        
        # For langchain-postgres, filters are simple key-value pairs
        # No need for $ prefixed operators - that was for the old langchain-community version
        pg_filter = filter  # Use filter directly
        
        # Retrieve documents
        initial_docs = self.vector_store.similarity_search(
            question, 
            k=self.initial_k, 
            filter=pg_filter
        )

        retrieved_docs = self._deduplicate_docs(initial_docs)
        logger.info(f"Retrieved {len(retrieved_docs)} unique documents for query")
        
        # Check relevance and build sources
        sources = []
        for doc in retrieved_docs:
            metadata = doc.metadata
            is_relevant, confidence, explanation = self._check_relevance(
                question,
                doc.page_content,
                metadata["idx"],
            )
            
            if is_relevant:
                source_info = {
                    "idx": str(metadata["idx"]),
                    "explanation": explanation,
                    "confidence": confidence
                }
                sources.append(source_info)
        
        logger.info(f"Found {len(sources)} relevant sources")
        return sources


def query_documents(question: str, knowledge_groups: list[str], db_manager: DatabaseManager, collection_name: str = "documents"):
    """Query the processed documents"""
    
    # Initialize components
    rag_core = RAGCore(db_manager, collection_name)
    query_engine = QueryEngine()
    
    # Load the existing vector store
    vector_store = rag_core.load_existing_vector_store()
    if not vector_store:
        logger.error("No vector store found. Please process documents first.")
        return []
    
    # Set up query engine
    query_engine.set_vector_store(vector_store)
    
    # Process query
    logger.info(f"Querying: {question}")
    sources = []
    
    for knowledge_id in knowledge_groups:
        try:
            results = query_engine.query(question, filter={"knowledge_id": knowledge_id})
            sources.extend(results)
        except Exception as e:
            logger.error(f"Error querying knowledge_id {knowledge_id}: {e}")
    
    return sources