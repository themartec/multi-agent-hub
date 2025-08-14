import requests
from settings import settings
import json

def get_all_items(base_url, headers=None):
    all_items = []
    current_page = 1
    has_more_pages = True
    
    while has_more_pages:
        try:
            response = requests.get(
                f"{base_url}?page={current_page}&per_page=100",
                headers=headers
            )
            response.raise_for_status()
            
            data = response.json()
            
            # print(data)
            
            # Thêm items vào list tổng
            all_items.extend(data.get('data', []))
            
            # Kiểm tra còn trang nào không
            if len(data.get('data', [])) < 100 or current_page >= data.get('total_pages', 1):
                has_more_pages = False
            else:
                current_page += 1
                
        except requests.exceptions.RequestException as e:
            print(f"Error fetching page {current_page}: {e}")
            break
    
    return all_items

# Sử dụng
all_data = get_all_items('https://apiuat.themartec.com/v1/story/getStoryResponsesGroupByAdvocate/d47b715f-1bda-4e7c-93dc-af97d19813ca', headers={
    "Authorization": f'Bearer {settings.AUTHEN_TOKEN}'
})

with open('responses_ibm.json', 'w') as fp:
    json.dump(all_data, fp)