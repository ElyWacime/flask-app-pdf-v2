from urllib import response
from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.files.file import File
import datetime
from dotenv import load_dotenv
import os

load_dotenv()

USERNAME = os.getenv('sharepoint_email')
PASSWORD = os.getenv('sharepoint_password')
SHAREPOINT_SITE = os.getenv('SHAREPOINT_SITE')
SHAREPOINT_SITE_NAME = os.getenv('SHAREPOINT_SITE_NAME')
SHAREPOINT_DOC = os.getenv('SHAREPOINT_DOC')

class SharePoint:
    def _auth(self):
        conn = ClientContext(SHAREPOINT_SITE).with_credentials(
            UserCredential(
                USERNAME,
                PASSWORD
            )
        )
        return conn

    def _get_files_list(self, folder_name):
        conn = self._auth()
        target_folder_url = f'{SHAREPOINT_DOC}/{folder_name}'
        root_folder = conn.web.get_folder_by_server_relative_url(target_folder_url)
        root_folder.expand(["Files", "Folders"]).get().execute_query()
        return root_folder.files
    
    def get_folder_list(self, folder_name):
        conn = self._auth()
        target_folder_url = f'{SHAREPOINT_DOC}/{folder_name}'
        root_folder = conn.web.get_folder_by_server_relative_url(target_folder_url)
        root_folder.expand(["Folders"]).get().execute_query()
        return root_folder.folders

    def download_file(self, file_name, folder_name):
        conn = self._auth()
        file_url = f'/sites/{SHAREPOINT_SITE_NAME}/{SHAREPOINT_DOC}/{folder_name}/{file_name}'
        file = File.open_binary(conn, file_url)
        return file.content
    
    def download_latest_file(self, folder_name):
        date_format = "%Y-%m-%dT%H:%M:%SZ"
        files_list = self._get_files_list(folder_name)
        file_dict = {}
        for file in files_list:
            dt_obj = datetime.datetime.strptime(file.time_last_modified, date_format)
            file_dict[file.name] = dt_obj
        # sort dict object to get the latest file
        file_dict_sorted = {key:value for key, value in sorted(file_dict.items(), key=lambda item:item[1], reverse=True)}    
        latest_file_name = next(iter(file_dict_sorted))
        content = self.download_file(latest_file_name, folder_name)
        return latest_file_name, content
        

    def upload_file(self, file_name, folder_name, content):
        conn = self._auth()
        target_folder_url = f'/sites/{SHAREPOINT_SITE_NAME}/{SHAREPOINT_DOC}/{folder_name}'
        target_folder = conn.web.get_folder_by_server_relative_path(target_folder_url)
        response = target_folder.upload_file(file_name, content).execute_query()
        return response
    
    def upload_file_in_chunks(self, file_path, folder_name, chunk_size, chunk_uploaded=None, **kwargs):
        conn = self._auth()
        target_folder_url = f'/sites/{SHAREPOINT_SITE_NAME}/{SHAREPOINT_DOC}/{folder_name}'
        target_folder = conn.web.get_folder_by_server_relative_path(target_folder_url)
        response = target_folder.files.create_upload_session(
            source_path=file_path,
            chunk_size=chunk_size,
            chunk_uploaded=chunk_uploaded,
            **kwargs
        ).execute_query()
        return response
    
    def get_list(self, list_name):
        conn = self._auth()
        target_list = conn.web.lists.get_by_title(list_name)
        items = target_list.items.get().execute_query()
        return items
        
    def get_file_properties_from_folder(self, folder_name):
        files_list = self._get_files_list(folder_name)
        properties_list = []
        for file in files_list:
            file_dict = {
                'file_id': file.unique_id,
                'file_name': file.name,
                'major_version': file.major_version,
                'minor_version': file.minor_version,
                'file_size': file.length,
                'time_created': file.time_created,
                'time_last_modified': file.time_last_modified
            }
            properties_list.append(file_dict)
            file_dict = {}
        return properties_list




# import os
# from office365.sharepoint.client_context import ClientContext
# from office365.runtime.auth.client_credential import ClientCredential
# from dotenv import load_dotenv

# load_dotenv()

# # SharePoint configuration
# SHAREPOINT_SITE = os.getenv('SHAREPOINT_SITE')
# CLIENT_ID = os.getenv('CLIENT_ID')
# CLIENT_SECRET = os.getenv('CLIENT_SECRET_VALUE')
# SHAREPOINT_DOC = os.getenv('SHAREPOINT_DOC')
# SHAREPOINT_SITE_NAME = os.getenv('SHAREPOINT_SITE_NAME')

# # Debugging prints to verify environment variables
# print(f"CLIENT_ID: {CLIENT_ID}")
# print(f"TENANT_ID: {os.getenv('TENANT_ID')}")
# print(f"CLIENT_SECRET: {CLIENT_SECRET}")

# class SharePoint:

#     def __init__(self):
#         self.site_url = SHAREPOINT_SITE
#         self.client_credentials = ClientCredential(CLIENT_ID, CLIENT_SECRET)
#         self.ctx = ClientContext(self.site_url).with_credentials(self.client_credentials)

#     def upload_file(self, local_file_path, folder_name):
#         target_folder_url = f'/sites/{SHAREPOINT_SITE_NAME}/{SHAREPOINT_DOC}/{folder_name}'
#         with open(local_file_path, 'rb') as file:
#             file_name = os.path.basename(local_file_path)
#             target_folder = self.ctx.web.get_folder_by_server_relative_url(target_folder_url)
#             target_file = target_folder.upload_file(file_name, file.read()).execute_query()
#             print(f"File {file_name} has been uploaded to {target_file.serverRelativeUrl}")

# if __name__ == "__main__":
#     sharepoint = SharePoint()
#     local_file_path = "./output_2025-02-26_20-39-55.pdf"  # Replace with your file path
#     folder_name = "Documents"  # Replace with your folder name
#     sharepoint.upload_file(local_file_path, folder_name)



# import os
# import requests
# from dotenv import load_dotenv

# load_dotenv()

# # SharePoint configuration
# SHAREPOINT_SITE = os.getenv('SHAREPOINT_SITE')
# SHAREPOINT_SITE_NAME = os.getenv('SHAREPOINT_SITE_NAME')
# CLIENT_ID = os.getenv('CLIENT_ID')
# TENANT_ID = os.getenv('TENANT_ID')
# CLIENT_SECRET = os.getenv('CLIENT_SECRET_VALUE')

# # Debugging prints to verify environment variables
# print(f"CLIENT_ID: {CLIENT_ID}")
# print(f"TENANT_ID: {TENANT_ID}")
# print(f"CLIENT_SECRET: {CLIENT_SECRET}")

# class SharePoint:

#     def get_folder_path(self, folder_name):
#         print(f"\n\n\n\n\n>>>>>>>>>>>>  {folder_name}  <<<<<<<<<<<<<\n\n\n\n")
#         folder_url = f"{SHAREPOINT_SITE}/_api/web/GetFolderByServerRelativeUrl('{folder_name}')"
#         print(f"\n\n\n\n\n>>>>>>>>>>>>  {folder_url}  <<<<<<<<<<<<<\n\n\n\n")
#         headers = {
#             "Authorization": f"Bearer {self._get_access_token()}",
#             "Accept": "application/json;odata=verbose"
#         }
#         response = requests.get(folder_url, headers=headers)
#         response.raise_for_status()
#         folder_data = response.json()
#         return folder_data['d']['ServerRelativeUrl']

#     def upload_file_via_api(self, local_file_path, folder_name):
#         folder_path = self.get_folder_path(folder_name)
#         upload_url = f"{SHAREPOINT_SITE}/_api/web/GetFolderByServerRelativeUrl('{folder_path}')/Files/add(url='{os.path.basename(local_file_path)}',overwrite=true)"
        
#         headers = {
#             "Authorization": f"Bearer {self._get_access_token()}",
#             "Accept": "application/json;odata=verbose",
#             "Content-Type": "application/octet-stream"
#         }

#         with open(local_file_path, 'rb') as file:
#             response = requests.post(upload_url, headers=headers, data=file)
        
#         if response.status_code == 200:
#             print("File uploaded successfully")
#         else:
#             print(f"Failed to upload file: {response.status_code}, {response.text}")

#     def _get_access_token(self):
#         url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
#         payload = {
#             'grant_type': 'client_credentials',
#             'client_id': CLIENT_ID,
#             'client_secret': CLIENT_SECRET,
#             'scope': f"{SHAREPOINT_SITE}/.default"
#         }
#         headers = {
#             "Content-Type": "application/x-www-form-urlencoded"
#         }
#         print(f"Payload: {payload}")  # Debugging print
#         response = requests.post(url, data=payload, headers=headers)
#         if response.status_code != 200:
#             print(f"Failed to get access token: {response.status_code}, {response.text}")
#         response.raise_for_status()
#         access_token = response.json().get('access_token')
#         print(f"Access token: {access_token}")  # Debugging print
#         return access_token
    
#     def get_folder_info(self, folder_name):
#         folder_url = f"{SHAREPOINT_SITE}/_api/web/GetFolderByServerRelativeUrl('{folder_name}')"
#         headers = {
#             "Authorization": f"Bearer {self._get_access_token()}",
#             "Accept": "application/json;odata=verbose"
#         }
#         print(f"Requesting folder info with URL: {folder_url}")  # Debugging print
#         response = requests.get(folder_url, headers=headers)
#         if response.status_code != 200:
#             print(f"Failed to get folder info: {response.status_code}, {response.text}")
#         response.raise_for_status()
#         folder_info = response.json()
#         return folder_info

