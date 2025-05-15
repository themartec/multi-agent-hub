from app.helpers.rag_core import RAGCore
import json
from dotenv import load_dotenv

# def process_documents(file_path: str, translate_to_english: bool = False):
#     """Process documents and create vector store
    
#     Args:
#         file_path: Path to the document file to process
#         translate_to_english: If True, translates documents to English before processing
    
#     Returns:
#         bool: True if processing was successful, False otherwise
#     """
    
#     # Load environment variables
#     load_dotenv()
    
#     # Initialize RAG system
#     rag_core = RAGCore()
    
#     try:
#         with open(file_path) as f:
#             stories = json.load(f)
    
#         documents = [(story["headline"], story["final_content"]) for story in stories]
        
#         # Format documents for processing
#         formatted_docs = []
#         for doc in documents:
#             if len(doc) == 2:  # Ensure document has all required parts
#                 formatted_docs.append(doc)
        
#         if not formatted_docs:
#             print("Error: No valid documents found in the file")
#             return False
            
#         print(f"\nProcessing {len(formatted_docs)} documents...")
#         if translate_to_english:
#             print("Translation to English enabled")
        
#         # Process the document list
#         vector_store = rag_core.process_document_list(
#             formatted_docs, 
#             translate_to_english=translate_to_english
#         )
        
#         print("\nDocument processing completed successfully!")
        
#     except Exception as e:
#         print(f"An error occurred during document processing: {str(e)}")

# if __name__ == "__main__":
#     file_path = "all_story_details.json"
#     translate_to_english = False
    
#     success = process_documents(file_path, translate_to_english)