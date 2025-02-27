import os
import requests
from dotenv import load_dotenv

load_dotenv()

# SharePoint configuration
SHAREPOINT_SITE = os.getenv('sharepoint_url_site')
SHAREPOINT_SITE_NAME = os.getenv('sharepoint_site_name')
SHAREPOINT_DOC = os.getenv('sharepoint_doc_library')
CLIENT_ID = os.getenv('CLIENT_ID')
TENANT_ID = os.getenv('TENANT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

class SharePoint:

    def get_folder_path(self, folder_name):
        folder_url = f"{SHAREPOINT_SITE}/_api/web/GetFolderByServerRelativeUrl('{SHAREPOINT_DOC}/{folder_name}')"
        headers = {
            "Authorization": f"Bearer {self._get_access_token()}",
            "Accept": "application/json;odata=verbose"
        }
        response = requests.get(folder_url, headers=headers)
        response.raise_for_status()
        folder_data = response.json()
        return folder_data['d']['ServerRelativeUrl']

    def upload_file_via_api(self, local_file_path, folder_name):
        folder_path = self.get_folder_path(folder_name)
        upload_url = f"{SHAREPOINT_SITE}/_api/web/GetFolderByServerRelativeUrl('{folder_path}')/Files/add(url='{os.path.basename(local_file_path)}',overwrite=true)"
        
        headers = {
            "Authorization": f"Bearer {self._get_access_token()}",
            "Accept": "application/json;odata=verbose",
            "Content-Type": "application/octet-stream"
        }

        with open(local_file_path, 'rb') as file:
            response = requests.post(upload_url, headers=headers, data=file)
        
        if response.status_code == 200:
            print("File uploaded successfully")
        else:
            print(f"Failed to upload file: {response.status_code}, {response.text}")

    def _get_access_token(self):
        url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
        payload = {
            'grant_type': 'client_credentials',
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'scope': f"{SHAREPOINT_SITE}/.default"
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        response = requests.post(url, data=payload, headers=headers)
        if response.status_code != 200:
            print(f"Failed to get access token: {response.status_code}, {response.text}")
        response.raise_for_status()
        return response.json().get('access_token')