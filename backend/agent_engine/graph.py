from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_google_genai import ChatGoogleGenerativeAI
from .state import AgentState
from .tools import drive_search_tool
from prompts.system_prompt import SYSTEM_PROMPT
from core.config import settings  # 📌 The Clerk arrives
from datetime import datetime

# 1. Setup the LLM dynamically using the SSOT
llm = ChatGoogleGenerativeAI(
    model=settings.MODEL_NAME, 
    api_key=settings.GOOGLE_API_KEY, # Production Hitch, resolve attempt 1
    temperature=settings.yaml_config['agent']['temperature'],
    timeout=settings.TIMEOUT
)
llm_with_tools = llm.bind_tools([drive_search_tool])
# 2. Define the "Thinking" node
def call_model(state: AgentState):
    current_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    prompt = SYSTEM_PROMPT.format(current_date=current_date)
    
    messages = [{"role": "system", "content": prompt}] + state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

# 3. Build the Graph
workflow = StateGraph(AgentState)

workflow.add_node("agent", call_model)
workflow.add_node("tools", ToolNode([drive_search_tool]))

workflow.set_entry_point("agent")

def should_continue(state: AgentState):
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    return END

workflow.add_conditional_edges("agent", should_continue)
workflow.add_edge("tools", "agent")

# Compile the pure logic
app = workflow.compile()