from langchain_core.tools import tool
import requests

from app.workflows.employer_branding_mvp.utils.tools import get_content_from_url
from settings import settings
from app.helpers.rag_core import query_documents

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
def get_content_from_library(request: str):
    """Always use this function to get the content when user want to repurpose the existing content from library"""
    return query_documents(request)

tools = [get_content_from_url, get_content_from_library]

