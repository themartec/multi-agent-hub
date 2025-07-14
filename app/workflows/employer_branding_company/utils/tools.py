from langchain_core.tools import tool
from langchain_core.runnables.config import RunnableConfig

from app.workflows.employer_branding_mvp.utils.tools import get_content_from_url
from app.helpers.rag_core import query_documents

@tool
def get_content_from_library(request: str, config: RunnableConfig):
    """Always use this function to get the content when user want to repurpose the existing content from library"""
    company_id = config.get("configurable", {}).get("company_id")
    return query_documents(request, company_id, "base_knowledge_graph")

tools = [get_content_from_url, get_content_from_library]
