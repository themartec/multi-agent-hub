from typing import Optional, List
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

import cohere

from settings import settings

class RAGCore:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small", api_key=settings.OPENAI_API_KEY)
        self.vector_store = None

    def process_document_list(self, documents: List[List], persist_directory: str = "./chroma_db", translate_to_english: bool = False) -> Chroma:
        """Process a list of documents where each document is [idx, knowledge_id, final_content, insight]"""
        print("\nProcessing documents...")
        
        processed_docs = []
        count = 0
        for doc in documents:
            if len(doc) != 4:
                print(f"Skipping invalid document format: {doc}")
                continue
                
            idx, knowledge_id, final_content, insight = doc
            
            # Create document with metadata
            doc_with_metadata = Document(
                page_content=insight,
                metadata={
                    "idx": idx,
                    "knowledge_id": knowledge_id,
                    "final_content": final_content
                }
            )
            processed_docs.append(doc_with_metadata)
            print(f"Processed document {idx}. Count: {count}")
            count += 1
        
        # Create and return the vector store
        self.vector_store = Chroma.from_documents(
            documents=processed_docs,
            embedding=self.embeddings,
            persist_directory=persist_directory,
            collection_metadata={"hnsw:space": "cosine"}  # Ensure proper distance metric
        )
        
        print(f"Created vector store with {len(processed_docs)} documents")
        return self.vector_store

    def get_vector_store(self):
        """Get the current vector store"""
        return self.vector_store

    def load_existing_vector_store(self, persist_directory: str = "./chroma_db"):
        """Load an existing vector store from disk"""
        self.vector_store = Chroma(
            embedding_function=self.embeddings,
            persist_directory=persist_directory
        )
        return self.vector_store

class QueryEngine:
    def __init__(self, vector_store: Optional[Chroma] = None, initial_k: int = 3):
        self.vector_store = vector_store
        self.initial_k = initial_k  # Number of initial documents to retrieve
        self.cohere_client = cohere.ClientV2(api_key=settings.COHERE_API_KEY)
        
    def set_vector_store(self, vector_store: Chroma):
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

    def _check_relevance(self, question: str, docs: list[str], relevance_threshold):
        """Check if a document is relevant to the question using cohere"""
        try:
            response = self.cohere_client.rerank(
                model="rerank-v3.5",
                query=question,
                documents=docs,
                top_n=5,
            )
            print(response.results)
            return [result.index for result in response.results if result.relevance_score >= relevance_threshold]
            
        except Exception as e:
            print(f"Error in relevance checking: {e}")
            return []

    def query(self, question: str, relevance_threshold: float = 0.5, filter = None):
        """Query the RAG system with LLM re-ranking. Returns both the answer and the sources used."""
        if not self.vector_store:
            raise ValueError("Vector store not set. Please set a vector store before querying.")
        
        # Retrieve and deduplicate initial set of documents
        initial_docs = self.vector_store.similarity_search(question, k=self.initial_k, filter=filter)
        retrieved_docs = self._deduplicate_docs(initial_docs)
        
        if not retrieved_docs:
            return []
        
        metadatas = [doc.metadata for doc in retrieved_docs]
        page_contents = [doc.page_content for doc in retrieved_docs]
        
        relevant_indexes = self._check_relevance(question, page_contents, relevance_threshold)
        # relevant_indexes = range(len(metadatas))
        
        sources = [
            {
                "idx": str(metadatas[index]["idx"]),
                "knowledge_id": str(metadatas[index]["knowledge_id"]),
                "final_content": metadatas[index]["final_content"]
            } for index in relevant_indexes
        ]

        return sources

def query_documents(question: str, knowledge_groups: list[str]):
    """Query the processed documents"""
    
    # Initialize components
    rag_core = RAGCore()
    query_engine = QueryEngine()
    
    # Load the existing vector store
    vector_store = rag_core.load_existing_vector_store()
    if not vector_store:
        print("Error: No vector store found. Please process documents first.")
        return
    
    # Set up query engine
    query_engine.set_vector_store(vector_store)
    
    # Process query
    print(f"\nQuestion: {question}")
    sources = []
    for knowledge_id in knowledge_groups:
        sources.extend(query_engine.query(question, filter={"knowledge_id": knowledge_id}))
    
    print(sources)
    
    return sources
