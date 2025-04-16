from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from app.workflows.employer_branding.utils.system_prompts import get_agent_system_message
from app.workflows.employer_branding.utils.tools import get_content_from_url

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import create_react_agent

load_dotenv()

model = ChatOpenAI(model="gpt-4o", api_key=os.getenv("OPENAI_API_KEY"))

checkpointer = InMemorySaver()

workflow = create_react_agent(
    model,
    [get_content_from_url],
    prompt=get_agent_system_message("employer_branding"),
    name="employer_branding",
    checkpointer=checkpointer
)