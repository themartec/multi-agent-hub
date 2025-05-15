import requests

def get_brand_guidelines(token):
    url = "https://apiuat.themartec.com/v1/company/getBrandGuidelinesByCompanyId"
    
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
            tovs = response['data']['data']['tone_content_a']
            
            compliance_content = response['data']['data']['compliance_content']
            
            terms = response['data']['data']['terms']
            evps = [element['value'] for element in terms if element['type'] == "EVP"]
            evps = ", ".join(evps)
            
            return tovs, compliance_content, evps
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
        
def get_company_info(token):
    url = "https://apiuat.themartec.com/v1/employee/getEmployeeProfileByAuth"
    
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
            first_name = response['data']['profile']['firstName']
            email = response['data']['profile']['email']
            company_name = response['data']['profile']['company']['name']
            return first_name, email, company_name
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