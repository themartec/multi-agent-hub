import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/..'))

from app.helpers.rag_core import query_documents
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Example usage
if __name__ == "__main__":
    # Query documents
    results = query_documents("carrer growth", company_id="e33f0667-ddb6-4375-8c3b-42d7aefc6f09", knowledge_graph_id="base_knowledge_graph")
    logger.info(f"Found {len(results)} relevant documents")
    
    print(results)