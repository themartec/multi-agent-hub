from langchain_core.tools import tool

from app.workflows.employer_branding_mvp.utils.tools import get_content_from_url
from app.helpers.rag_core import query_documents

from langchain_core.runnables.config import RunnableConfig


#
# @tool
# def get_content_from_url(raw_url: str):
#     """Always use this function to crawl the content when user input the URL"""
#     url = f"https://r.jina.ai/{raw_url}"
#     headers = {
#         "Authorization": f'Bearer {settings.JINA_API_KEY}'
#     }
#
#     response = requests.get(url, headers=headers)
#
#     return response.text

@tool
def query_knowledge_base(request: str, config: RunnableConfig):
    """Always use this function to get user's knowledge base."""
    
    knowledge_groups = config.get("configurable", {}).get("knowledge_groups", [])
    if not knowledge_groups:
        return
    
    return query_documents(request, knowledge_groups)

tools = [get_content_from_url, query_knowledge_base]
