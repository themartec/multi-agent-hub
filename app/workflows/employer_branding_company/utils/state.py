from langgraph.graph import MessagesState
from typing import List

class State(MessagesState):
    tovs: str
    compliance_content: str
    evps: str
    first_name: str
    email: str
    company_name: str
    ui: List[dict]
    english_type: str
    knowledge_groups: List[str]