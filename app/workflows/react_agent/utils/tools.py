from dotenv import load_dotenv
from langchain_core.tools import tool
import os
import requests

load_dotenv()

@tool
def get_content_from_url(raw_url: str):
    """Use this to crawl the content when user input the URL"""
    url = f"https://r.jina.ai/{raw_url}"
    headers = {
        "Authorization": f'Bearer {os.getenv("JINA_API_KEY")}'
    }

    response = requests.get(url, headers=headers)
    
    return response.text


tools = [get_content_from_url]