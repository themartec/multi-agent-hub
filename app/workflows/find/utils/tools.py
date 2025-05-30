from langchain_core.tools import tool

from app.workflows.employer_branding_mvp.utils.tools import get_content_from_url
from app.helpers.rag_core import DatabaseManager, query_documents

from langchain_core.runnables.config import RunnableConfig

@tool
def query_knowledge_base(request: str, config: RunnableConfig):
    """Always use this function to get user's knowledge base."""
    
    knowledge_groups = config.get("configurable", {}).get("knowledge_groups", [])
    if not knowledge_groups:
        return
    
    db_manager = DatabaseManager()
    try:
        # Query documents
        results = query_documents(request, knowledge_groups, db_manager, "knowledge_base_collection")
    finally:
        # Clean up
        db_manager.close()
    
    return results

tools = [get_content_from_url, query_knowledge_base]
