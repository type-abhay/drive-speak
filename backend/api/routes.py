from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from agent_engine.graph import app  # 🧠 This is your LangGraph agent
from langchain_core.messages import HumanMessage

router = APIRouter()

# 1. Define the Input Schema
class ChatRequest(BaseModel):
    query: str

@router.post("/chat")
async def chat_with_agent(request: ChatRequest):
    """
    The main interface for the Streamlit frontend. 
    It parses natural language and strictly returns the final text.
    """
    if not request.query:
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    try:
        # 1. Prepare the Initial State
        inputs = {"messages": [HumanMessage(content=request.query)]}
        
        # 2. Invoke the Graph
        result = app.invoke(inputs)
        
        # 3. Extract the raw content
        raw_content = result["messages"][-1].content
        final_text = ""
        
        # 4. The Purifier: Handle complex structured responses
        if isinstance(raw_content, str):
            final_text = raw_content
            
        elif isinstance(raw_content, list):
            # Extract ONLY the blocks explicitly marked as 'text'
            text_blocks = [
                block["text"] for block in raw_content 
                if isinstance(block, dict) and block.get("type") == "text"
            ]
            final_text = "\n\n".join(text_blocks)
            
        else:
            # Fallback for completely unexpected structures
            final_text = str(raw_content)
        
        return {"status": "success", "response": final_text.strip()}
        
    except Exception as e:
        print(f"❌ Error in Agent Logic: {e}")
        raise HTTPException(status_code=500, detail="The agent encountered a logical fracture.")
# Keep your old search endpoint for debugging if you like
@router.post("/search")
async def execute_raw_search(query: ChatRequest):
    # This is for raw q-parameter testing
    from services.drive_service import drive_client
    files = drive_client.search_files(request.query)
    return {"status": "success", "files": files}