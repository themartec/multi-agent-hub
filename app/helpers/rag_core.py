from typing import Optional, List, Tuple
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
import chromadb
from langchain_chroma import Chroma
from langchain_core.documents import Document

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
import logging

from settings import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RAGCore:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(
            api_key=settings.OPENAI_API_KEY,
            model="text-embedding-3-large"
        )
        # self.chroma_client = chromadb.CloudClient(
        #     api_key=settings.CHROMA_API_KEY,
        #     tenant=settings.CHROMA_TENANT,
        #     database=settings.CHROMA_DATABASE
        # )
        self.vector_store = None

    def process_document_list(self, documents: List[List], company_id: str, knowledge_graph_id: str) -> Chroma:
        """Process a list of documents where each document is [index, category, text]"""
        print("\nProcessing documents...")
        
        processed_docs = []
        for doc in documents:
            if len(doc) != 2:
                print(f"Skipping invalid document format: {doc}")
                continue
                
            content, metadata = doc
            
            # Create document with metadata
            doc_with_metadata = Document(
                page_content=content,
                metadata=metadata
            )
            processed_docs.append(doc_with_metadata)
            print(f"Processed Story: {metadata['story_id']}")
        
        print("Start returning the vector store")
        # Create and return the vector store
        self.vector_store = Chroma.from_documents(
            # client=self.chroma_client,
            documents=processed_docs,
            embedding=self.embeddings,
            collection_name=f"{company_id}-{knowledge_graph_id}",
            persist_directory="chroma_db",
            collection_metadata={"hnsw:space": "cosine"}  # Ensure proper distance metric
        )
        
        print(f"Created vector store with {len(processed_docs)} documents")
        return self.vector_store

    def get_vector_store(self):
        """Get the current vector store"""
        return self.vector_store

    def load_existing_vector_store(self, company_id, knowledge_graph_id):
        """Load an existing vector store from disk"""
        self.vector_store = Chroma(
            embedding_function=self.embeddings,
            persist_directory="chroma_db",
            collection_name=f"{company_id}-{knowledge_graph_id}"
        )
        return self.vector_store

class RelevanceResponse(BaseModel):
    """Structure for relevance scoring response"""
    is_relevant: bool
    confidence: float
    explanation: str

class QueryEngine:
    def __init__(self, vector_store: Optional[Chroma] = None, initial_k: int = 5):
        self.vector_store = vector_store
        self.initial_k = initial_k  # Number of initial documents to retrieve
        
        # Create the relevance checking prompt
        self.relevance_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert at determining whether a content is relevant to a given question.
            Analyze the content carefully and determine if it contains information that would help answer the question.
            Consider both direct answers and contextually relevant information."""),
            ("user", """Question: {question}

content:
[Headline: {story_title}]
{content}

Determine if this content is relevant to answering the question. Provide:
1. is_relevant: true/false
2. confidence: Score between 0 and 1
3. explanation: Brief explanation of your decision""")
        ])
        
        # Initialize the LLMs
        self.relevance_llm = ChatOpenAI(
            model="gpt-4.1",
            temperature=0,
            api_key=settings.OPENAI_API_KEY
        ).with_structured_output(RelevanceResponse).with_config(
            config={"tags": ["langsmith:nostream"]}
        )

    def set_vector_store(self, vector_store: Chroma):
        """Set the vector store to use for queries"""
        self.vector_store = vector_store

    def _deduplicate_docs(self, docs):
        """Deduplicate documents based on their index"""
        seen_indices = set()
        unique_docs = []
        
        for doc in docs:
            story_title = doc.metadata.get("story_title")
            if story_title not in seen_indices:
                seen_indices.add(story_title)
                unique_docs.append(doc)
        
        return unique_docs

    def _check_relevance(self, question: str, doc_content: str, story_title: str) -> Tuple[bool, float]:
        """Check if a document is relevant to the question using LLM"""
        try:
            response = self.relevance_llm.invoke(
                self.relevance_prompt.format(
                    question=question,
                    story_title=story_title,
                    content=doc_content
                )
            )
            print(f"Relevant: {response.is_relevant}, Confidence: {response.confidence}")
            print(f"Explanation: {response.explanation}")
            return response.is_relevant, response.confidence, response.explanation
        except Exception as e:
            print(f"Error in relevance checking: {e}")
            return False, 0.0

    def query(self, question: str, relevance_threshold: float = 0.7):
        """Query the RAG system with LLM re-ranking. Returns both the answer and the sources used."""
        if not self.vector_store:
            raise ValueError("Vector store not set. Please set a vector store before querying.")
        
        # Retrieve and deduplicate initial set of documents
        initial_docs = self.vector_store.similarity_search(question, k=self.initial_k)

        retrieved_docs = self._deduplicate_docs(initial_docs)
        
        # Format context with document metadata and check relevance
        sources = []
        
        for doc in retrieved_docs:
            metadata = doc.metadata
            # Check relevance using LLM
            is_relevant, confidence, explanation = self._check_relevance(
                question,
                doc.page_content,
                metadata["story_title"],
            )
            
            # Only include relevant documents that meet the threshold
            if is_relevant and confidence >= relevance_threshold:
                source_info = {
                    "story_title": str(metadata["story_title"]),
                    "content": doc.page_content,
                    "explanation": explanation
                }
                sources.append(source_info)
                
        return sources

def query_documents(question: str, company_id: str, knowledge_graph_id: str):
    """Query the processed documents"""
    # Load environment variables
    load_dotenv()
    
    # Initialize components
    rag_core = RAGCore()
    query_engine = QueryEngine()
    
    # Load the existing vector store
    vector_store = rag_core.load_existing_vector_store(company_id, knowledge_graph_id)
    if not vector_store:
        print("Error: No vector store found. Please process documents first.")
        return
    
    # Set up query engine
    query_engine.set_vector_store(vector_store)

    # Process query
    print(f"\nQuestion: {question}")
    sources = query_engine.query(question)

    return sources
