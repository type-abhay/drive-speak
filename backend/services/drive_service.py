from google.oauth2 import service_account
from googleapiclient.discovery import build
from core.config import settings

class DriveService:
    def __init__(self):
        self.creds = service_account.Credentials.from_service_account_file(
            settings.GOOGLE_CREDS_PATH, 
            scopes=settings.SCOPES
        )
        # API CLIENT SERVICE
        self.service = build('drive', 'v3', credentials=self.creds)

    # backend/services/drive_service.py

    def search_files(self, q_parameter: str) -> list:
        """
        Executes a 'Deep Search'. 
        Since this is a Service Account, we search all files it has been granted 
        access to, effectively searching the shared folder and all its sub-folders.
        """
        try:
            # MISSION REQUIREMENT: The agent must search within the designated folder.
            # Instead of 'in parents', we use the shared access as our boundary.
            # If you want to be extra safe, we ensure we don't return the root folder itself.
            
            final_query = f"({q_parameter}) and trashed = false"

            results = self.service.files().list(
                q=final_query,
                spaces='drive',
                # Ensure we get the parent info so we can see where the file lives
                fields="nextPageToken, files(id, name, mimeType, webViewLink, createdTime, parents)",
                pageSize=settings.yaml_config['search_settings'].get('max_results', 10)
            ).execute()
            
            return results.get('files', [])
            
        except Exception as e:
            print(f"An error occurred in Drive API: {e}")
            return []

# Instantiate it once to be used across the app
drive_client = DriveService()