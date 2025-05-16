import json

import requests
from settings import settings


class TheMartecSecret:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.token_martec = cls._instance.get_token_platform()
        return cls._instance

    def get_token_platform(self):
        endpoint = "https://apiuat.themartec.com/v1"
        endpoint_csrf = f"{endpoint}/session/generate-csrf-token"
        response = requests.request("GET",
                                    endpoint_csrf,
                                    headers={'Content-Type': 'application/json'})
        assert response.status_code == 200, f"csrf token getting status code is {response.status_code}"
        csrf_token = response.json()["data"]["token"]
        assert csrf_token, f"csrf_token is empty"
        payload = json.dumps(
            {"email": settings.USER_NAME,
             "password": settings.USER_PWD,
             "allowSwitchAdvocate": "false",
             "token": csrf_token
             })
        endpoint_login = f"{endpoint}/auth/login"
        response = requests.request("POST",
                                    endpoint_login,
                                    headers={'Content-Type': 'application/json'},
                                    data=payload)
        assert response.status_code == 200, f"bear token getting status code is {response.status_code}"
        bear_token = response.json()["data"]["token"]
        return bear_token


def get_brand_guidelines(token):
    url = "https://apiuat.themartec.com/v1/company/getBrandGuidelinesByCompanyId"

    # Headers with Bearer token
    headers = {
        "Authorization": f"Bearer {TheMartecSecret().token_martec}"
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
        "Authorization": f"Bearer {TheMartecSecret().token_martec}"
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