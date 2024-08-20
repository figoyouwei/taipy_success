'''
@author: Youwei Zheng
@target: 天眼查内容返回成功并优化
@update: 2024.08.01
'''

import os
import requests
import json

from dotenv import load_dotenv
load_dotenv()

import os
import requests
from urllib.parse import quote

def tyc_baseinfo_normal(company_name: str):
    """
    Fetches the profile information from Tianyancha API for a given company name.

    Args:
        company_name (str): The name of the company to fetch information for.

    Returns:
        dict: A dictionary containing the company's profile information if the request was successful.
        None: If there was an error or the request failed.
    """
    
    TYC_API_URL = "http://open.api.tianyancha.com/services/open/ic/baseinfo/normal"

    if not company_name:
        return None

    encoded_company_name = quote(company_name)
    profile_url = f"{TYC_API_URL}?keyword={encoded_company_name}"

    token = os.getenv('TYC_TOKEN')
    if not token:
        raise ValueError("TYC_TOKEN environment variable is not set.")

    headers = {'Authorization': token}

    try:
        response = requests.get(profile_url, headers=headers)
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code

        # Assuming the API returns JSON data
        return response.json()
    except requests.RequestException as e:
        print(f"Request error: {e}")
        return None
    except ValueError as e:
        print(f"Invalid response: {e}")
        return None

# ------------------------------
# Main.app
# ------------------------------

if __name__ == "__main__":
    res = tyc_baseinfo_normal("上海棱逊科技有限公司")
    res['result']['alias']
    # print(json.loads(response.text))