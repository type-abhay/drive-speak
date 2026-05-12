from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    # This stores the entire back-and-forth conversation
    # add_messages ensures new messages are appended, not overwritten
    messages: Annotated[Sequence[BaseMessage], add_messages]