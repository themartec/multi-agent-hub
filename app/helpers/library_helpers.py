import requests

def create_library_item(token, payload):
    # API endpoint
    url = "https://apiuat.themartec.com/v1/library/create"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    # Make the POST request
    response = requests.post(url, headers=headers, json=payload)
    
    # Check response
    if response.status_code == 200:
        print("Request successful!")
        print(response.json())  # Print the response JSON
    else:
        print(f"Request failed with status code: {response.status_code}")
        print(response.text)  # Print the error message
    
    return response


import time
import json
import os

def get_all_library_stories(token, base_url, initial_per_page=50, output_file="all_stories.json"):
    """
    Fetch all library stories from the API using pagination and save to a JSON file
    
    Args:
        base_url (str): Base URL of the API without query parameters
        initial_per_page (int): Initial number of items per page (default: 50)
        output_file (str): Path to the output JSON file
    
    Returns:
        int: Number of stories saved to the file
    """
    all_stories = []
    current_page = 1
    total_stories = None
    per_page = initial_per_page
    
    print(f"Starting to fetch stories from {base_url}")
    print(f"Results will be saved to {output_file}")
    
    # Headers with Bearer token
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    while True:
        # Construct the URL with pagination parameters
        url = f"{base_url}?page={current_page}&per_page={per_page}"
        
        try:
            # Make API request
            print(f"Fetching page {current_page} with {per_page} items per page...")
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise exception for HTTP errors
            
            data = response.json()
            
            # Extract stories and pagination info
            stories = data.get('data', [])
            pagination = data.get('paginate', {})
            
            # Get total stories count if not yet known
            if total_stories is None:
                total_stories = pagination.get('total', 0)
                print(f"Total stories to fetch: {total_stories}")
            
            # Add stories to our collection
            all_stories.extend(stories)
            print(f"Fetched page {current_page}, got {len(stories)} stories. Total collected: {len(all_stories)}/{total_stories} ({round(len(all_stories)/total_stories*100, 2)}%)")
            
            # Check if we've fetched all stories
            if len(all_stories) >= total_stories:
                break
                
            # Move to next page
            current_page += 1
            
            # Small delay to avoid overloading the server
            time.sleep(0.2)
            
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error while fetching page {current_page}: {e}")
            
            # If we get an error due to per_page being too large, reduce it and retry
            if response.status_code == 400 and per_page > 10:
                per_page = per_page // 2
                print(f"Reducing per_page to {per_page} and retrying")
                continue
            else:
                # For other errors, break the loop
                print("Could not resolve the error. Saving what we've collected so far.")
                break
                
        except requests.exceptions.RequestException as e:
            print(f"Request Exception while fetching page {current_page}: {e}")
            print("Saving what we've collected so far.")
            break
    
    # Create result object with metadata
    result = {
        "metadata": {
            "total_stories": total_stories,
            "collected_stories": len(all_stories),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "source": base_url
        },
        "stories": all_stories
    }
    
    # Save to file with pretty formatting
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        # Get file size
        file_size = os.path.getsize(output_file) / (1024 * 1024)  # Size in MB
        print(f"Successfully saved {len(all_stories)} stories to {output_file} ({file_size:.2f} MB)")
        
    except Exception as e:
        print(f"Error saving to file: {e}")
        
        # Try to save to a backup file with a different name
        backup_file = f"backup_{int(time.time())}_stories.json"
        print(f"Attempting to save to backup file: {backup_file}")
        
        try:
            with open(backup_file, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(f"Successfully saved to backup file {backup_file}")
        except Exception as e2:
            print(f"Error saving to backup file: {e2}")
    
    return len(all_stories)

def get_story_detail(token, story_id):
    url = f"https://apiuat.themartec.com/v1/story/getStoryResponsesGroupByAdvocate/{story_id}?page=1"
    
    # Headers with Bearer token
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        # send request GET
        response = requests.get(url, headers=headers)
        
        # Check the status of the response
        if response.status_code == 200:
            response = response.json()
            return response
        else:
            return {
                "success": False,
                "status_code": response.status_code,
                "message": f"Error: {response.text}"
            }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error occurred: {str(e)}"
        }