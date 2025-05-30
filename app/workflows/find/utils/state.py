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
    task: str
    output: str
    source_content: str
    knowledge_groups: List[str]
    task_description: str
    task_instruction: str