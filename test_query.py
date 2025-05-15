from typing import Optional, List, Tuple
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_chroma import Chroma
from pydantic import BaseModel, Field
    
from dotenv import load_dotenv
from app.helpers.rag_core import RAGCore

class SourceInfo(BaseModel):
    """Structure for source information"""
    headline: str = Field(description="The headline of the source document")
    final_content: str = Field(description="Preview of the source text"),
    explanation: str = Field(description="Explanation of the relevance check")

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
            ("system", """You are an expert at determining whether a article is relevant to a given question.
            Analyze the content carefully and determine if it contains information that would help answer the question.
            Consider both direct answers and contextually relevant information."""),
            ("user", """Question: {question}

Article:
[Headline: {headline}]
{content}

Determine if this article is relevant to answering the question. Provide:
1. is_relevant: true/false
2. confidence: Score between 0 and 1
3. explanation: Brief explanation of your decision""")
        ])
        
        # Initialize the LLMs
        self.relevance_llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0,
        ).with_structured_output(RelevanceResponse)

    def set_vector_store(self, vector_store: Chroma):
        """Set the vector store to use for queries"""
        self.vector_store = vector_store

    def _deduplicate_docs(self, docs):
        """Deduplicate documents based on their index"""
        seen_indices = set()
        unique_docs = []
        
        for doc in docs:
            headline = doc.metadata.get("headline")
            if headline not in seen_indices:
                seen_indices.add(headline)
                unique_docs.append(doc)
        
        return unique_docs

    def _check_relevance(self, question: str, doc_content: str, headline: str) -> Tuple[bool, float]:
        """Check if a document is relevant to the question using LLM"""
        try:
            response = self.relevance_llm.invoke(
                self.relevance_prompt.format(
                    question=question,
                    headline=headline,
                    content=doc_content
                )
            )
            print(f"Relevant: {response.is_relevant}, Confidence: {response.confidence}")
            print(f"Explanation: {response.explanation}")
            return response.is_relevant, response.confidence, response.explanation
        except Exception as e:
            print(f"Error in relevance checking: {e}")
            return False, 0.0

    def query(self, question: str, relevance_threshold: float = 0.7) -> List[SourceInfo]:
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
                metadata["headline"],
            )
            
            # Only include relevant documents that meet the threshold
            if is_relevant and confidence >= relevance_threshold:
                source_info = SourceInfo(
                    headline=str(metadata["headline"]),
                    final_content=doc.page_content,
                    explanation=explanation
                )
                sources.append(source_info)
                
        print("lennnnn", len(sources))
                
        return sources

def query_documents(question: str):
    """Query the processed documents"""
    # Load environment variables
    load_dotenv()
    
    # Initialize components
    rag_core = RAGCore()
    query_engine = QueryEngine()
    
    try:
        # Load the existing vector store
        vector_store = rag_core.load_existing_vector_store()
        if not vector_store:
            print("Error: No vector store found. Please process documents first.")
            return
        
        # Set up query engine
        query_engine.set_vector_store(vector_store)
        
        # Process query
        print(f"\nQuestion: {question}")
        sources = query_engine.query(question)
        
        print(sources)

    except Exception as e:
        print(f"An error occurred during querying: {str(e)}")

if __name__ == "__main__":
    # Example usage
    question = "mentor in gallagher"
    query_documents(question)