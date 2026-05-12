# backend/test_drive.py
import os
from services.drive_service import drive_client
from core.config import settings

def test_connection():
    print("Attempting logic check run..")
    
    if not settings.GOOGLE_CREDS_PATH:
        print("Error: GOOGLE_APPLICATION_CREDENTIALS not found in .env")
        return
    
    print(f"Found Creds Path: {settings.GOOGLE_CREDS_PATH}")
    print(f"Target Folder ID: {settings.TARGET_FOLDER_ID}")

    # 2. Attempt a simple list operation
    print("\nAttempting connection with Drive..")    
    # Passing an empty name search which will be combined with folder constraint in drive_service
    results = drive_client.search_files("name contains ''")
    
    if results:
        print(f"Success! Let's go!! Found {len(results)} files in the shared folder:")
        for file in results:
            print(f" - {file['name']} (ID: {file['id']}, Type: {file['mimeType']})")
    else:
        print(" [!] Connection worked, directory empty though.")
        print("Does the shared account have accees?")

if __name__ == "__main__":
    test_connection()