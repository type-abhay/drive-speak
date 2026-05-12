import os
from dotenv import load_dotenv

load_dotenv()
class Settings:
    GOOGLE_CREDS_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    TARGET_FOLDER_ID = os.getenv("DRIVE_FOLDER_ID")
    # The exact scope required for read-only access to Drive files
    SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

settings = Settings()