from langchain_core.tools import tool
from services.drive_service import drive_client
from core.config import settings

@tool
def drive_search_tool(q_string: str):
    """
    Search for files in Google Drive using a structured query string.
    The 'q_string' must follow the Google Drive API 'q' parameter format.
    """
    # The drive_client inherently respects the TARGET_FOLDER_ID from config
    print(f"📊 Query: {q_string}")
    results = drive_client.search_files(q_string)
    
    if not results:
        return "No files found for that query. Try broadening your search."
    
    # We can also use config to limit how many results we feed back to the LLM
    max_items = settings.yaml_config['search_settings'].get('max_results', 10)
    limited_results = results[:max_items]
    
    formatted_results = "\n".join([
        f"- {f['name']} (ID: {f['id']}, Link: {f['webViewLink']})" 
        for f in limited_results
    ])
    return f"I found these files:\n{formatted_results}"