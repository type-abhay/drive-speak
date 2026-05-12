from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.drive_service import drive_client

router = APIRouter()

# Define the expected structure of the incoming request
class SearchQuery(BaseModel):
    q_string: str

@router.post("/search")
async def execute_search(query: SearchQuery):
    """
    Endpoint that accepts a raw 'q' string from the agent
    and returns the discovered files.
    """
    if not query.q_string:
        raise HTTPException(status_code=400, detail="Query string cannot be empty.")
    
    files = drive_client.search_files(query.q_string)
    return {"status": "success", "files": files}