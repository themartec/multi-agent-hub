from app.helpers.rag_core import RAGCore
import json
from dotenv import load_dotenv
import os

def process_documents(company_name, company_id: str):
        # Load environment variables
    load_dotenv()
    
    # Initialize RAG system
    rag_core = RAGCore()
    
    try:
        with open(f"all_stories_{company_name}.json") as f:
            all_stories = json.load(f)
            
        documents = []

        proceed_stories = os.listdir(f"data/{company_name}")
        proceed_stories = [story.split(".")[0] for story in  proceed_stories]
        
        proceed_stories_responses = os.listdir(f"data/{company_name}_responses")

        documents = []
        for story in all_stories["stories"]:
            metadata = {}
            metadata["story_id"] = story["id"]
            metadata["story_title"] = story["headline"]
            metadata["created_time"] = story["created_at"]
            metadata["content_source"] = story["content_type"]
            metadata["content_format"] = story["type"]
            metadata["status"] = story["status"]
            metadata["doc_type"] = "article"
            metadata["company_id"] = company_id
            if story["id"] in proceed_stories:
                with open(f"data/{company_name}/{story['id']}.txt") as f:
                    content = f.read()
            else:
                content = story["headline"] + "\n"
                if story["advocates"]:
                    content += "Advocate:\n"
                    for advocate in story["advocates"]:
                        first_name = "Name: " + advocate["user"]["first_name"] + " " if advocate["user"]["first_name"] else ""
                        last_name = advocate["user"]["last_name"] + ". " if advocate["user"]["last_name"] else ""
                        email = "Email: " + advocate["user"]["email"] if advocate["user"]["email"] else ""
                        content += first_name + last_name + email + "\n"
                if story["tags"]:
                    content += "Tags: "
                    tags = [tag["name"] for tag in story["tags"]]
                    content += ", ".join(tags)
                    
            document = [content, metadata]
            documents.append(document)
            
        for story in all_stories["stories"]:
            if story["id"] in proceed_stories_responses:
                metadata = {}
                metadata["story_id"] = story["id"]
                metadata["story_title"] = story["headline"]
                metadata["created_time"] = story["created_at"]
                metadata["content_source"] = story["content_type"]
                metadata["content_format"] = story["type"]
                metadata["status"] = story["status"]
                metadata["doc_type"] = "responses"
                metadata["company_id"] = company_id
                
                response_ids = os.listdir(f"data/{company_name}_responses/{story['id']}")
                response_ids = [response_id.replace(".txt", "") for response_id in response_ids]
                for response_id in response_ids:
                    metadata["response_id"] = response_id
                    with open(f"data/{company_name}_responses/{story['id']}/{response_id}.txt") as f:
                        content = f.read()
                    document = [content, metadata]
                    documents.append(document)
            
        # Format documents for processing
        formatted_docs = []
        for doc in documents:
            if len(doc) == 2:  # Ensure document has all required parts
                formatted_docs.append(doc)
        
        if not formatted_docs:
            print("Error: No valid documents found in the file")
            return False
            
        print(f"\nProcessing {len(formatted_docs)} documents...")
        
        # Process the document list
        vector_store = rag_core.process_document_list(
            formatted_docs,
            company_id=company_id,
            knowledge_graph_id="base_knowledge_graph"
        )
        
        print("\nDocument processing completed successfully!")
        
    except Exception as e:
        print(f"An error occurred during document processing: {str(e)}")

if __name__ == "__main__":
    success = process_documents("ibm", "e33f0667-ddb6-4375-8c3b-42d7aefc6f09")