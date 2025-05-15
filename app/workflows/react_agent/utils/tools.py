from langchain_core.tools import tool
import requests
from settings import settings

@tool
def get_content_from_url(raw_url: str):
    """Use this to crawl the content when user input the URL"""
    url = f"https://r.jina.ai/{raw_url}"
    headers = {
        "Authorization": f'Bearer {settings.JINA_API_KEY}'
    }

    response = requests.get(url, headers=headers)
    
    return response.text


tools = [get_content_from_url]