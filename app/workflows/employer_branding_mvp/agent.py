import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langgraph.prebuilt import create_react_agent
from app.schemas.models import OpenAIModelName
from app.workflows.employer_branding_mvp.utils.system_prompts import get_agent_system_message
from app.workflows.employer_branding_mvp.utils.tools import get_content_from_url

load_dotenv()

workflow = create_react_agent(
    ChatOpenAI(model=OpenAIModelName.GPT_41,
               api_key=os.getenv("OPENAI_API_KEY")),
    [get_content_from_url],
    prompt=get_agent_system_message("employer_branding_mvp_plus"),
    name="employer_branding_mvp",
)


