from urllib import response
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.file import File
import datetime
from dotenv import load_dotenv
import os
from office365.runtime.auth.client_credential import ClientCredential

load_dotenv()

USERNAME = os.getenv('SHAREPOINT_EMAIL')
PASSWORD = os.getenv('SHAREPOINT_PASS')
SHAREPOINT_SITE = os.getenv('SHAREPOINT_SITE')
SHAREPOINT_SITE_NAME = os.getenv('SHAREPOINT_SITE_NAME')
SHAREPOINT_DOC = os.getenv('SHAREPOINT_DOC')

# Add these environment variables
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET_VALUE')

class SharePoint:
    def _auth(self):
        try:
            client_credentials = ClientCredential(CLIENT_ID, CLIENT_SECRET)
            ctx = ClientContext(SHAREPOINT_SITE).with_credentials(client_credentials)
            return ctx
        except Exception as e:
            print(f"Error authenticating: {e}")
            raise

    def upload_file(self, file_name, folder_name, content):
        conn = self._auth()
        # Modified to use the root-relative path
        target_folder_url = f'{SHAREPOINT_DOC}/{folder_name}'
        target_folder = conn.web.get_folder_by_server_relative_path(target_folder_url)
        response = target_folder.upload_file(file_name, content).execute_query()
        return response
    
    def upload_file_in_chunks(self, file_path, folder_name, chunk_size, chunk_uploaded=None, **kwargs):
        conn = self._auth()
        # Modified to use the root-relative path
        target_folder_url = f'{SHAREPOINT_DOC}/{folder_name}'
        target_folder = conn.web.get_folder_by_server_relative_path(target_folder_url)
        response = target_folder.files.create_upload_session(
            source_path=file_path,
            chunk_size=chunk_size,
            chunk_uploaded=chunk_uploaded,
            **kwargs
        ).execute_query()
        return response
