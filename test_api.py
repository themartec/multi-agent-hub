from dotenv import load_dotenv
import os
import requests
import json

load_dotenv()

def get_top_10_google(keyword: str):
    """Use this to recommend top 10 google when user input the keywords"""
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'q': keyword,
        'key': os.getenv("GOOGLE_SEARCH_API_KEY"),
        'cx': os.getenv("GOOGLE_SEARCH_ID"),
        'num': 10  # Request only top 10 results
    }
    
    try:
        # Make the request
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Extract search results
        search_results = response.json()
        
        # Extract only the relevant information from the top 3 results
        top_results = []
        if 'items' in search_results:
            for item in search_results['items'][:3]:
                result = {
                    'title': item.get('title', ''),
                    'link': item.get('link', ''),
                    'snippet': item.get('snippet', '')
                }
                top_results.append(result)
                
        return top_results
                
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return []
    except (KeyError, json.JSONDecodeError) as e:
        print(f"Error processing results: {e}")
        return []
    
print(get_top_10_google("bitcoin price today"))