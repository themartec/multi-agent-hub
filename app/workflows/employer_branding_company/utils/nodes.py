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
from app.helpers.rag_core import query_documents
from settings import settings

import uuid

tools_by_name = {tool.name: tool for tool in tools}

model = ChatOpenAI(model="gpt-4.1", api_key=settings.OPENAI_API_KEY)


def get_user_info(state: State):
    tovs, compliance_content, evps = get_brand_guidelines(settings.AUTHEN_TOKEN)
    first_name, email, company_name = get_company_info(settings.AUTHEN_TOKEN)
    text_list = state["messages"][-1].content.split()
    knowledge_groups = [text.replace("@@", "@") for text in text_list if "@@" in text]
    
    for knowledge_id in knowledge_groups:
        state["messages"][-1].content = state["messages"][-1].content.replace(f"@{knowledge_id}", "").strip()
    
    english_type = EnglishStyle.AMERICAN

    return {
        "tovs": tovs,
        "compliance_content": compliance_content,
        "evps": evps,
        "first_name": first_name,
        "email": email,
        "company_name": company_name,
        "english_type": english_type,
        "knowledge_groups": knowledge_groups
    }


def first_route(state: State):
    if len(state["messages"]) <= 1:
        return "yes"
    elif state["messages"][-1].content == "/save_to_library":
        return "save_to_library"
    else:
        return "no"


# Define our tool node
def tool_node(state: State):
    outputs = []
    for tool_call in state["messages"][-1].tool_calls:
        tool_result = tools_by_name[tool_call["name"]].invoke(tool_call["args"], config={"configurable": {"knowledge_groups": state["knowledge_groups"]}})
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
    tool_model = model.bind_tools(tools)
    # this is similar to customizing the create_react_agent with 'prompt' parameter, but is more flexible
    system_prompt = SystemMessage(get_agent_system_message("employer_branding_mvp_plus").format(
        eb_first_name=state['first_name'],
        eb_email=state['email'],
        company_name=state['company_name'],
        company_tone=state['tovs'],
        brand_compliance=state['compliance_content'],
        company_evp=state['evps'],
        english_type=state['english_type']
    )
    )
    
    # state["messages"][-1].content = state["messages"][-1].content + ". Refer to knowledge base to create answer."
    
    response = tool_model.invoke([system_prompt] + state["messages"], config)
    
    artifact_id = "artifact_ui_" + str(uuid.uuid4())
    
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
