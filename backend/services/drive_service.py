from google.oauth2 import service_account
from googleapiclient.discovery import build
from core.config import settings
import json # Add this import at the top

class DriveService:
    def __init__(self):
        if settings.GOOGLE_CREDS_JSON:
            # Production: Read from environment variable string
            creds_dict = json.loads(settings.GOOGLE_CREDS_JSON)
            self.creds = service_account.Credentials.from_service_account_info(
                creds_dict, scopes=settings.SCOPES
            )
        else:
            # Local: Read from file path
            self.creds = service_account.Credentials.from_service_account_file(
                settings.GOOGLE_CREDS_PATH, scopes=settings.SCOPES
            )

        self.service = build('drive', 'v3', credentials=self.creds)

    # backend/services/drive_service.py

    def search_files(self, q_parameter: str) -> list:
        """
        Executes a 'Deep Search'. 
        Since this is a Service Account, we search all files it has been granted 
        access to, effectively searching the shared folder and all its sub-folders.
        """
        try:            
            final_query = f"({q_parameter}) and trashed = false"

            results = self.service.files().list(
                q=final_query,
                spaces='drive',
                #getting parent info so we can see where the file lives
                fields="nextPageToken, files(id, name, mimeType, webViewLink, createdTime, parents)",
                pageSize=settings.yaml_config['search_settings'].get('max_results', 10)
            ).execute()
            
            return results.get('files', [])
            
        except Exception as e:
            print(f"An error occurred in Drive API: {e}")
            return []

drive_client = DriveService()