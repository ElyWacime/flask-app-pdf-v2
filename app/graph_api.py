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
    print(f"Access Token: {access_token}")  # Debugging print
    return access_token

def get_site_id(access_token, site_name):
    url = "https://graph.microsoft.com/v1.0/sites"
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    sites = response.json().get('value', [])
    for site in sites:
        if site.get('name') == site_name:
            print(f"Site ID: {site.get('id')}")  # Debugging print
            return site.get('id')
    raise Exception(f"Site '{site_name}' not found")

def get_drive_id(access_token, site_id):
    url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drives"
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    drives = response.json().get('value', [])
    if drives:
        print(f"Drive ID: {drives[0].get('id')}")  # Debugging print
        return drives[0].get('id')
    raise Exception("No drives found")

def get_folder_id(access_token, site_id, drive_id, folder_path):
    url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drives/{drive_id}/root:/{folder_path}:/children"
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    items = response.json().get('value', [])
    for item in items:
        if item.get('name') == os.path.basename(folder_path) and item.get('folder'):
            print(f"Folder ID: {item.get('id')}")  # Debugging print
            return item.get('id')
    raise Exception(f"Folder '{folder_path}' not found")
