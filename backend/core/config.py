import os
import yaml
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

class Settings:
    def __init__(self):
        # 1. Load Secrets from .env
        self.GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
        self.GOOGLE_CREDS_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        self.SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

        # 2. Load Behavioral Config from YAML
        config_path = Path(__file__).parent.parent / "config.yaml"
        with open(config_path, "r") as f:
            self.yaml_config = yaml.safe_load(f)

        # 3. Flatten for easy access
        self.MODEL_NAME = self.yaml_config['agent']['model']
        self.TIMEOUT = self.yaml_config['agent']['timeout_seconds']
        self.TARGET_FOLDER_ID = self.yaml_config['search_settings']['target_folder_id']

settings = Settings()