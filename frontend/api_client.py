import os
import requests
from dotenv import load_dotenv

load_dotenv()

# We pull the URL from the .env file
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000/api/v1/chat")

def send_query_to_backend(user_text: str) -> str:
    """
    Transmits the natural language query to the FastAPI backend and extracts the response.
    """
    try:
        payload = {"query": user_text}
        response = requests.post(BACKEND_URL, json=payload, timeout=60)
        
        # Raise an exception if the HTTP request failed
        response.raise_for_status()
        
        data = response.json()
        
        # Assuming your FastAPI endpoint returns a JSON with a 'response' key
        return data.get("response", "No readable response was returned from the agent.")
        
    except requests.exceptions.ConnectionError:
        return "⚠️ **System Offline:** Could not connect to the backend forge. Is FastAPI running?"
    except requests.exceptions.Timeout:
        return "⏳ **Timeout:** The agent took too long to scour the digital repository."
    except Exception as e:
        return f"❌ **Anomaly Detected:** {str(e)}"