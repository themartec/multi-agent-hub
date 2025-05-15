from app.helpers.get_brand_guidelines import get_brand_guidelines, get_company_info
from app.helpers.library_helpers import create_library_item, get_all_library_stories, get_story_detail
from settings import settings
import requests
from io import BytesIO
import docx

def read_docx_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        doc = docx.Document(BytesIO(response.content))
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        
        return '\n'.join(full_text)
    else:
        return f"Error: {response.status_code}"


# tovs, compliance_content, evps = get_brand_guidelines(settings.AUTHEN_TOKEN)
# first_name, email, company_name = get_company_info(settings.AUTHEN_TOKEN)

# print(tovs, compliance_content, evps)
# print(first_name, email, company_name)

# print(create_library_item())

get_all_library_stories(settings.AUTHEN_TOKEN, "https://apiuat.themartec.com/v1/story/getLibraryStoryList", 50)

import json

with open('all_stories.json') as f:
    original_stories = json.load(f)
    
stories_id = [story["id"] for story in original_stories["stories"] if story["status"] == "FINAL" and story["type"] == "WRITTEN"]
story_type = [story["type"] for story in original_stories["stories"] if story["status"] == "FINAL" and story["type"] == "WRITTEN"]
story_headline = [story["headline"] for story in original_stories["stories"] if story["status"] == "FINAL" and story["type"] == "WRITTEN"]
urls = [story["written"]["file_url"] for story in original_stories["stories"] if story["status"] == "FINAL" and story["type"] == "WRITTEN"]
final_content = []

for url in urls:
    final_content.append(read_docx_from_url(url))

all_stories = []

for i, idx in enumerate(stories_id):
    story_detail = get_story_detail(settings.AUTHEN_TOKEN, idx)
    all_stories.append({
        "id": idx,
        "type": story_type[i],
        "headline": story_headline[i],
        "final_content": final_content[i]
    })
    
with open('all_story_details.json', 'w') as fp:
    json.dump(all_stories, fp)