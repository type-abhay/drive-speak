# backend/test_agent.py
import os
from langgraph.graph import StateGraph
from langchain_core.messages import HumanMessage
from langgraph.graph import END

# Import the compiled graph from your structure
from agent_engine.graph import app
from core.config import settings

def run_agent_test(query: str):
    print(f"--- 🧠 Testing Agent with Query: '{query}' ---")
    
    # 1. Initialize the state with the user's message
    initial_state = {
        "messages": [HumanMessage(content=query)]
    }

    # 2. Invoke the Graph
    # This will trigger the agent -> tool -> agent loop
    print("📡 Agent is thinking and executing tools...")
    
    try:
        # We use stream to see the steps as they happen
        for output in app.stream(initial_state):
            for key, value in output.items():
                print(f"\n[Node: {key}]")
                last_message = value["messages"][-1]
                
                # Check if the LLM called a tool
                if hasattr(last_message, "tool_calls") and last_message.tool_calls:
                    for tool_call in last_message.tool_calls:
                        print(f"🛠️  Tool Called: {tool_call['name']}")
                        print(f"📊 Generated 'q' string: {tool_call['args'].get('q_string')}")
                else:
                    print(f"💬 Response: {last_message.content}")

        print("\n--- ✅ Test Complete ---")
        
    except Exception as e:
        print(f"\n❌ Error during graph execution: {e}")

if __name__ == "__main__":
    # Test Case 1: Simple discovery
    run_agent_test("Find me all PDF files in the folder.")
    
    # Test Case 2: Complex intent (Date + Name)
    # This checks if the LLM uses the system prompt's current_date logic
    # run_agent_test("Are there any documents about 'financials' from this week?")