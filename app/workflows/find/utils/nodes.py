from langchain_openai import ChatOpenAI
import json
from langchain_core.messages import ToolMessage, SystemMessage
from langchain_core.runnables import RunnableConfig

from app.helpers.get_brand_guidelines import get_brand_guidelines, get_company_info
from app.schemas.settings import EnglishStyle
from app.workflows.find.utils.system_prompts import find_prompt_v1
from app.workflows.find.utils.state import State
from app.workflows.find.utils.tools import tools
from app.workflows.find.utils.constant import task_descriptions_dict, task_instructions_dict
from settings import settings

import uuid

tools_by_name = {tool.name: tool for tool in tools}

model = ChatOpenAI(model="gpt-4.1", api_key=settings.OPENAI_API_KEY)

def get_user_info(state: State):
    tovs, compliance_content, evps = get_brand_guidelines(settings.AUTHEN_TOKEN)
    first_name, email, company_name = get_company_info(settings.AUTHEN_TOKEN)
    
    first_message = state["messages"][-1].content
    task = first_message.split("\n")[0].split(": ")[1].strip()
    output = first_message.split("\n")[1].split(": ")[1].strip()
    source_content = first_message.split("\n")[2].split(": ")[1].strip()
    other_instruction = first_message.split("\n")[3].split(": ")[1].strip()
    extra_tovs = first_message.split("\n")[4].split(": ")[1]
    tovs = tovs + ", " + extra_tovs
    knowledge_groups = first_message.split("\n")[5].split(": ")[1].split(", ")
    knowledge_groups = ["@"+knowledge_group for knowledge_group in knowledge_groups]
    task_description = task_descriptions_dict[task][output]
    task_instruction = task_instructions_dict[task][output]
    task_instruction = task_instruction + "\n" + other_instruction
    
    english_type = EnglishStyle.AMERICAN

    return {
        "tovs": tovs,
        "compliance_content": compliance_content,
        "evps": evps,
        "first_name": first_name,
        "email": email,
        "company_name": company_name,
        "english_type": english_type,
        "task": task,
        "output": output,
        "source_content": source_content,
        "knowledge_groups": knowledge_groups,
        "task_description": task_description,
        "task_instruction": task_instruction
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
    system_prompt = SystemMessage(find_prompt_v1.format(
        eb_first_name=state['first_name'],
        eb_email=state['email'],
        company_name=state['company_name'],
        company_tone=state['tovs'],
        brand_compliance=state['compliance_content'],
        company_evp=state['evps'],
        english_type=state['english_type'],
        task=state['task'],
        output=state['output'],
        task_description=state['task_description'],
        task_instruction=state['task_instruction']
    )
    )
    
    state["messages"][-1].content = state["messages"][-1].content + "\nRefer to knowledge base to create answer."
    
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
