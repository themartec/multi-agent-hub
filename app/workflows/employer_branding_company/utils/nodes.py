from langchain_openai import ChatOpenAI
import json
from langchain_core.messages import ToolMessage, SystemMessage, AIMessage, HumanMessage
from langchain_core.runnables import RunnableConfig

from app.helpers.get_brand_guidelines import get_brand_guidelines, get_company_info
from app.helpers.library_helpers import create_library_item
from app.schemas.settings import EnglishStyle
from app.workflows.employer_branding_company.utils.system_prompts import get_agent_system_message
from app.workflows.employer_branding_company.utils.state import State
from app.workflows.employer_branding_company.utils.tools import tools
from app.workflows.employer_branding_company.utils.schema import AgentResponse
from settings import settings

import uuid

tools_by_name = {tool.name: tool for tool in tools}

model = ChatOpenAI(model="gpt-4.1", api_key=settings.OPENAI_API_KEY)

def get_user_info(state: State):
    company_id=state["messages"][1].content.split("\n")[-1].split("- Company ID: ")[-1]

    return {
        "company_id": company_id
    }


def first_route(state: State):
    if len(state["messages"]) <= 3:
        return "yes"
    elif state["messages"][-1].content == "/save_to_library":
        return "save_to_library"
    else:
        return "no"


# Define our tool node
def tool_node(state: State):
    outputs = []
    for tool_call in state["messages"][-1].tool_calls:
        tool_result = tools_by_name[tool_call["name"]].invoke(tool_call["args"], config={"configurable": {"company_id": state["company_id"]}})
        outputs.append(
            ToolMessage(
                content=json.dumps(tool_result),
                name=tool_call["name"],
                tool_call_id=tool_call["id"],
            )
        )
    return {"messages": outputs}


# Define the node that calls the model
def call_model(
        state: State,
        config: RunnableConfig,
):
    if len(state["messages"]) <= 3:
        state["company_id"] = state["messages"][1].content.split("\n")[-1].split("- Company ID: ")[-1]

    tool_model = model.bind_tools(tools)
    # this is similar to customizing the create_react_agent with 'prompt' parameter, but is more flexible
    system_prompt = SystemMessage(get_agent_system_message("employer_branding_mvp_v4")
                                  # .format(
                                  #     eb_first_name=state['first_name'],
                                  #     eb_email=state['email'],
                                  #     company_name=state['company_name'],
                                  #     company_tone=state['tovs'],
                                  #     brand_compliance=state['compliance_content'],
                                  #     company_evp=state['evps'],
                                  #     english_type=state['english_type']
                                  # )
                                  # try:
                                  )
    # except:
    #     system_prompt = SystemMessage(get_agent_system_message("employer_branding_mvp_plus").format(
    #         eb_first_name="Test Admin",
    #         eb_email="admin@eb.com",
    #         company_name="Gallagher",
    #         company_tone="open, honest, friendly, human-like, use contractions",
    #         brand_compliance="""phrases like "colleagues are like family", "we want you to bring your "whole self" to work""",
    #         company_evp="culture of excellence, collaboration, career growth and learning,belonging, authenticity",
    #         english_type='AMERICAN English'
    #     )
    #     )
    artifact_id = "artifact_ui_" + str(uuid.uuid4())

    response = tool_model.invoke([system_prompt] + state["messages"], config)
    # We return a list, because this will get added to the existing list
    return {
        "messages": [response],
        "ui": [
            {
                "id": artifact_id,
                "type": "custom_artifact_display",
                "metadata": {
                    "message_id": response.id
                },
                "data": {
                    "title": f"Title of {artifact_id}",
                    "children": f"Content of {artifact_id}"
                }
            }
        ]
    }


# Define the conditional edge that determines whether to continue or not
def should_continue(state: State):
    messages = state["messages"]
    last_message = messages[-1]
    # If there is no function call, then we finish
    if not last_message.tool_calls:
        return "end"
    # Otherwise if there is, we continue
    else:
        return "continue"


def save_to_library(state: State):
    state["messages"][-1].content = "Please help me save the content into the library"
    structured_model = model.with_structured_output(AgentResponse).with_config(
        config={"tags": ["langsmith:nostream"]}
    )
    system_prompt = get_agent_system_message("content_extraction")
    response = structured_model.invoke(
        [SystemMessage(content=system_prompt), HumanMessage(content=state["messages"][-2].content)])

    payload = {
        "status": "RAW",
        "asset_upload_type": "PLAIN_TEXT",
        "headline": response.headline,
        "file_link": "",
        "content": response.content,
        "content_type": "WRITTEN",
        "category_id": "574a809f-6125-4e44-8d26-3e732b76b9f8",
        "publish_date": None,
        "tag_selection": []
    }

    create_library_item(settings.AUTHEN_TOKEN, payload)

    return {"messages": [AIMessage("Done!")]}
