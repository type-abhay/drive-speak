# backend/core/config.py
import os
import yaml
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Settings:
    def __init__(self):
        # 1. Load Secrets/Overrides from .env
        self.GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
        self.GOOGLE_CREDS_JSON = os.getenv("GOOGLE_CREDENTIALS_JSON") # For Cloud
        self.GOOGLE_CREDS_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS") # For Local
        self.SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
        
        # 2. Load Defaults from YAML
        config_path = Path(__file__).parent.parent / "config.yaml"
        with open(config_path, "r") as f:
            self.yaml_config = yaml.safe_load(f)

        # 3. Smart Flattening (Environment Overrides YAML)
        self.MODEL_NAME = self.yaml_config['agent']['model']
        self.TIMEOUT = self.yaml_config['agent']['timeout_seconds']
        
        # Priority: Env Variable > config.yaml
        env_folder_id = os.getenv("DRIVE_FOLDER_ID")
        yaml_folder_id = self.yaml_config['search_settings'].get('target_folder_id')
        self.TARGET_FOLDER_ID = env_folder_id or yaml_folder_id

settings = Settings()