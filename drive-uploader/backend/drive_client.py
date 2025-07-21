import os
import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

class DriveClient:
    SCOPES = ['https://www.googleapis.com/auth/drive.file']

    def __init__(self, client_id=None, client_secret=None, project_id=None, redirect_uri='urn:ietf:wg:oauth:2.0:oob', credentials=None):
        creds = credentials
        if not creds:
            token_path = 'token.json'
            if os.path.exists(token_path):
                creds = Credentials.from_authorized_user_file(token_path, self.SCOPES)

            if not creds or not creds.valid:
                flow = InstalledAppFlow.from_client_config(
                    {
                        "installed": {
                            "client_id": client_id,
                            "client_secret": client_secret,
                            "redirect_uris": [redirect_uri],
                            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                            "token_uri": "https://oauth2.googleapis.com/token"
                        }
                    },
                    scopes=self.SCOPES
                )
                creds = flow.run_console()
                with open(token_path, 'w') as token_file:
                    token_file.write(creds.to_json())

        self.service = build('drive', 'v3', credentials=creds)

    def create_folder(self, name, parent_id=None):
        file_metadata = {
            'name': name,
            'mimeType': 'application/vnd.google-apps.folder',
        }
        if parent_id:
            file_metadata['parents'] = [parent_id]
        folder = self.service.files().create(body=file_metadata, fields='id').execute()
        return folder.get('id')

    def upload_file(self, local_path, drive_folder_id):
        file_metadata = {
            'name': os.path.basename(local_path),
            'parents': [drive_folder_id]
        }
        media_body = MediaFileUpload(local_path, resumable=True)
        file = self.service.files().create(
            body=file_metadata, media_body=media_body, fields='id'
        ).execute()
        return file.get('id')