import requests
import os
from dotenv import load_dotenv

load_dotenv()

TENANT_ID = os.getenv('TENANT_ID')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET_VALUE')


def get_access_token():
    url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'scope': 'https://graph.microsoft.com/.default'
    }
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    access_token = response.json().get('access_token')
    return access_token


def get_site_id(access_token, site_name):
    url = "https://graph.microsoft.com/v1.0/sites"
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        sites = response.json().get('value', [])
        for site in sites:
            if site.get('name') == site_name:
                print(f"Site ID: {site.get('id')}")  # Debugging print
                return site.get('id')
    except Exception as e:
        print(f"Error getting site ID: {e}")
    raise Exception(f"Site '{site_name}' not found")


def get_drive_id(access_token, site_id):
    url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drives"
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        drives = response.json().get('value', [])
        if drives:
            print(f"Drive ID: {drives[0].get('id')}")  # Debugging print
            return drives[0].get('id')
    except Exception as e:
        print(f"Error getting drive ID: {e}")
    raise Exception("No drives found")


def get_folder_id(access_token, site_id, drive_id, folder_path):
    url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drives/{drive_id}/root/children"
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        items = response.json().get('value', [])
        for item in items:
            if item.get('name') == os.path.basename(folder_path) and item.get('folder'):
                print(f"Folder ID: {item.get('id')}")  # Debugging print
                return item.get('id')
    except Exception as e:
        print(f"Error getting folder ID: {e}")
    raise Exception(f"Folder '{folder_path}' not found")


###################################################
##### YOU SHOULD TAKE A LOOK AT THIS FUNCTION #####
###################################################


import requests
import os

def upload_file_to_sharepoint(access_token, site_id, drive_id, folder_path, file_path):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/octet-stream'
    }
    
    file_name = os.path.basename(file_path)
    upload_url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drives/{drive_id}/root:/{folder_path}/{file_name}:/content"
    
    with open(file_path, 'rb') as file:
        response = requests.put(upload_url, headers=headers, data=file)
    
    response.raise_for_status()
    print(f"File uploaded successfully: {response.json()}")
    return response.json()

# Example usage
if __name__ == "__main__":
    access_token = get_access_token()
    site_id = get_site_id(access_token, os.getenv('SHAREPOINT_SITE_NAME'))
    drive_id = get_drive_id(access_token, site_id)
    folder_path = "Documents partages/09-Projets/AAA_FOR_TEST_TO_DELETE_LATER"  # Adjust the folder path as needed
    file_path = "/path/to/your/file.txt"  # Adjust the file path as needed
    
    upload_file_to_sharepoint(access_token, site_id, drive_id, folder_path, file_path)