from app.helpers.get_brand_guidelines import get_brand_guidelines, get_company_info
from app.helpers.library_helpers import create_library_item, get_all_library_stories, get_story_detail
from app.helpers.content_filttering import filter_content
from app.workflows.employer_branding_mvp.utils.tools import get_content_from_url
from settings import settings
import requests
from io import BytesIO
import docx
from get_all_response import get_all_items
import os

def get_original_url(shortened_url):
    try:
        response = requests.head(shortened_url, allow_redirects=True, timeout=10)
        return response.url
    except requests.exceptions.RequestException as e:
        print(f"Error when accessing the url: {e}")
        return None

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

# get_all_library_stories(settings.AUTHEN_TOKEN, "https://apiuat.themartec.com/v1/story/getLibraryStoryList", 50)

import json

company = 'ibm'

with open(f'all_stories_{company}.json') as f:
    original_stories = json.load(f)
    
# stories_id = [story["id"] for story in original_stories["stories"] if "written" in story]
# story_type = [story["type"] for story in original_stories["stories"] if "written" in story]
# story_headline = [story["headline"] for story in original_stories["stories"] if "written" in story]
# written_item = [story["written"] for story in original_stories["stories"] if "written" in story]
# final_content = []
# all_stories = []

# for i, idx in enumerate(stories_id):
#     print(idx, written_item[i]["type"])
#     if written_item[i]["type"] ==  "UPLOAD":
#         content = read_docx_from_url(written_item[i]["file_url"])
#     elif written_item[i]["type"] ==  "LINK":
#         content = get_content_from_url(written_item[i]["file_url"])
#         content = filter_content(content)
#     elif written_item[i]["type"] == "PLAIN_TEXT":
#         content = written_item[i]["content"]
#     elif written_item[i]["published_link"]:
#         content = get_content_from_url(written_item[i]["file_url"])
#     with open(f"data/marriott/{idx}.txt", "w") as f:
#         f.write(content)
    
# with open('all_story_details.json', 'w') as fp:
#     json.dump(all_stories, fp)
    
# url = "https://apiuat.themartec.com/v1/tag/get-list-for-library"

# headers = {
#     "Authorization": f"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImdhbGxhZ2hlckB0aGVtYXJ0ZWMuY29tIiwiYXV0aF9pZCI6IjgyYmE2MjhlLTI1MDgtNDA4ZS1iODZkLWQzYjBmM2UwODk1MiIsImNvbXBhbnlfaWQiOiJlYTRiNzFmNi00ZjViLTQwYjAtYWE3My1mZmU3ZjlkYzMyMzciLCJjb21wYW55X25hbWUiOiJHYWxsYWdoZXIiLCJhdWQiOiJCcm93c2VyIiwicGxhdGZvcm0iOiJFTVBMT1lFUiIsImlhdCI6MTc1MTM5NDIzMSwiZXhwIjoxNzUxNDgwNjMxfQ.el3k5eb2_-WE07cYQ-ujcIXcN3QDe1g_yTxHkGfW37M"
# }

# response = requests.get(url, headers=headers)
# response.raise_for_status()  # Raise exception for HTTP errors

# print(response.json())

# stories_id = [story["id"] for story in original_stories["stories"] if "video" in story and story["video"]["transcript"] and len(story["video"]["transcript"]) > 10]
# story_type = [story["type"] for story in original_stories["stories"] if "video" in story and story["video"]["transcript"] and len(story["video"]["transcript"]) > 10]
# story_headline = [story["headline"] for story in original_stories["stories"] if "video" in story and story["video"]["transcript"] and len(story["video"]["transcript"]) > 10]
# video_item = [story["video"] for story in original_stories["stories"] if "video" in story and story["video"]["transcript"] and len(story["video"]["transcript"]) > 10]

# for i, idx in enumerate(stories_id):
#     print(i, video_item[i]["type"])
#     content = video_item[i]["transcript"]
#     with open(f"data/marriott/{idx}.txt", "w") as f:
#         f.write(content)

# stories_id = [story["id"] for story in original_stories["stories"] if "video" in story and (not story["video"]["transcript"] or len(story["video"]["transcript"]) <= 10)]
# story_type = [story["type"] for story in original_stories["stories"] if "video" in story and (not story["video"]["transcript"] or len(story["video"]["transcript"]) <= 10)]
# story_headline = [story["headline"] for story in original_stories["stories"] if "video" in story and (not story["video"]["transcript"] or len(story["video"]["transcript"]) <= 10)]
# video_item = [story["video"] for story in original_stories["stories"] if "video" in story and (not story["video"]["transcript"] or len(story["video"]["transcript"]) <= 10)]

# for i, idx in enumerate(stories_id):
#     try:
#         url = get_original_url(video_item[i]["video_url"])
#         print(idx, video_item[i]["type"], url)
#         if 'youtube' in url or 'youtu.be' in url:
#             content = get_content_from_url(url)
#             with open(f"data/marriott/{idx}.txt", "w") as f:
#                 f.write(content)
#     except:
#         pass

# stories_id = [story["id"] for story in original_stories["stories"] if "written" not in story and "video" not in story and story["status"]=="FINAL"]
# story_type = [story["type"] for story in original_stories["stories"] if "written" not in story and "video" not in story and story["status"]=="FINAL"]
# story_headline = [story["headline"] for story in original_stories["stories"] if "written" not in story and "video" not in story and story["status"]=="FINAL"]
# stories_item = [story for story in original_stories["stories"] if "written" not in story and "video" not in story and story["status"]=="FINAL"]

# for i, idx in enumerate(stories_id):
#     if stories_item[i]["published_link"]:
#         print(i, idx, stories_item[i]["type"])
#         if stories_item[i]["type"] == "WRITTEN":
#             content = get_content_from_url(stories_item[i]["published_link"])
#             content = filter_content(content)
#             with open(f"data/ibm/{idx}.txt", "w") as f:
#                 f.write(content)
#         elif stories_item[i]["type"] == "VIDEO":
#             try:
#                 url = get_original_url(stories_item[i]["published_link"])
#                 if 'youtube' in url or 'youtu.be' in url:
#                     content = get_content_from_url(url)
#                     with open(f"data/ibm/{idx}.txt", "w") as f:
#                         f.write(content)
#             except:
#                 pass
        

# import os
# proceed_stories = os.listdir("data/marriott")
# proceed_stories = [story.split(".")[0] for story in  proceed_stories]

# final_stories = []

# for story in original_stories["stories"]:
#     print(story["id"])
#     item = {}
#     item["advocates"] = story["advocates"]
#     item["story_title"] = story["headline"]
#     item["created_time"] = story["created_at"]
#     item["content_source"] = story["content_type"]
#     item["content_format"] = story["type"]
#     item["status"] = story["status"]
#     item["tags"] = story["tags"]
#     if story["id"] in proceed_stories:
#         with open(f"data/marriott/{story['id']}.txt") as f:
#             item["content"] = f.read()
#     else:
#         item["content"] = story["headline"] + "\n"
#         if story["advocates"]:
#             item["content"] += "Advocate:\n"
#             for advocate in story["advocates"]:
#                 first_name = "Name: " + advocate["user"]["first_name"] + " " if advocate["user"]["first_name"] else ""
#                 last_name = advocate["user"]["last_name"] + ". " if advocate["user"]["last_name"] else ""
#                 email = "Email: " + advocate["user"]["email"] if advocate["user"]["email"] else ""
#                 item["content"] += first_name + last_name + email + "\n"
#         if story["tags"]:
#             item["content"] += "Tags: "
#             tags = [tag["name"] for tag in story["tags"]]
#             item["content"] += ", ".join(tags)
            
#     final_stories.append(item)

# with open('final_stories.json', 'w') as fp:
#     json.dump(final_stories, fp)

stories_id = [story["id"] for story in original_stories["stories"] if story["content_type"] == "STORY"]
story_type = [story["type"] for story in original_stories["stories"] if story["content_type"] == "STORY"]
story_headline = [story["headline"] for story in original_stories["stories"] if story["content_type"] == "STORY"]
stories_item = [story for story in original_stories["stories"] if story["content_type"] == "STORY"]

for i, idx in enumerate(stories_id):
    print(f"{i}/{len(stories_id)}", idx)
    all_responses = get_all_items(f'https://apiuat.themartec.com/v1/story/getStoryResponsesGroupByAdvocate/{idx}', headers={
        "Authorization": f'Bearer {settings.AUTHEN_TOKEN}'
    })
    if not all_responses:
        continue
    
    for advocate_item in all_responses:
        qna = advocate_item["question_answers"]
        if not qna:
            continue
        os.makedirs(f'data/{company}_responses/{idx}', exist_ok=True)
        for response in qna:
            response_id = response["id"]
            if stories_item[i]["type"] == "WRITTEN":
                answer = response["answer"]
            else:
                answer = response["story_videos"][-1]["transcript"]
            content = f"""Question: {response['question']}\n\nAnswer: {answer}"""
            with open(f"data/{company}_responses/{idx}/{response_id}.txt", "w") as f:
                f.write(content)