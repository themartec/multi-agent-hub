import json

from langchain_core.messages import HumanMessage, AIMessage
from langgraph.constants import END
from langgraph.graph import MessagesState, StateGraph
from langgraph.types import interrupt, Command
from app.workflows.eb_form_chat.agents import writer
from app.workflows.eb_form_chat.mapping_task import mapping_task
from app.workflows.react_agent.configuration import Configuration


def route_after_interrupt(state):
    return "end"


def human_edit(state):
    messages = state["messages"]
    human_msg = messages[-2].content
    print(f"human_msg: {human_msg}")
    msg_list = []
    for message in messages:
        if isinstance(message, HumanMessage):
            msg_list.append({"role": "user", "content": message.content})
        elif isinstance(message, AIMessage):
            msg_list.append({"role": "ai_assistant", "content": message.content})
    task_type = mapping_task(msg_list)
    print(f"task: {task_type}")
    is_skip = False
    special_msg = "I would like to ignore this template, and start with my own"
    for message in state["messages"]:
        # print(f"message: {message}")
        if isinstance(message, HumanMessage) and special_msg in message.content:
            is_skip = True
            break

    if task_type == "Content Create" and is_skip is not True:
        result = interrupt(
            {
                "action_request": {
                    "action": "Generate Content Template",
                    "args": {"topic": "Life At Sanofi",
                             "audience": "internal employees",
                             "sourceContent": "https://www.youtube.com/watch?v=AUd1NEdomlM"},
                },
                "description": "Please provide you inputs",
                "config": {
                    "allow_ignore": True,
                    "allow_respond": False,
                    "allow_edit": True,
                    "allow_accept": False,
                },
            }
        )
        human_action = result[0]["type"]
        if human_action == "edit":
            result_data = json.dumps(result[0])
            json_data = json.loads(result_data)
            args_data = json_data["args"]["args"]

            topic = args_data["topic"]
            audience = args_data["audience"]
            sourceContent = args_data["sourceContent"]
            return Command(goto="writer", update={
                "messages": [HumanMessage(content=f"Based on this initial inputs for writing:\n"
                                                  f"Topic: {topic}\n"
                                                  f"Audience: {audience}\n"
                                                  f"Source Content: {sourceContent}")]})
        elif human_action == "ignore":
            return Command(goto="writer", update={"messages": [HumanMessage(content="I would like to "
                                                                                    "ignore this template, "
                                                                                    "and start with my own"
                                                                                    "")]})
        else:
            # Need to update logic here
            return Command(goto="writer")
    elif task_type == "Augmented Job Create" and is_skip is not True:
        result = interrupt(
            {
                "action_request": {
                    "action": "Augmented Job Template",
                    "args": {
                        "source": "<URL/plaintext content>",
                        "language": "<used language>"}
                },
                "description": """Please provide you inputs:
                - Language: language of the content, by default English""",
                "config": {
                    "allow_ignore": False,
                    "allow_respond": False,
                    "allow_edit": True,
                    "allow_accept": False,
                },
            }
        )
        result_data = json.dumps(result[0])
        json_data = json.loads(result_data)
        args_data = json_data["args"]["args"]
        source = args_data["source"]
        language = args_data["language"]
        if result:
            return Command(goto="writer",
                           update={"messages": [HumanMessage(content=f"Based on this initial inputs for writing:\n"
                                                                     f"Source: {source}\nLanguage: {language}")]})
        else:
            # Need to update logic here
            return Command(goto="writer")
    else:
        print("continue here")
        # return Command(goto="writer")


def human_respond(state):
    return Command(goto="writer")


graph_builder = StateGraph(MessagesState, config_schema=Configuration)
graph_builder.add_node("writer", writer)
graph_builder.add_node("human_edit", human_edit)
graph_builder.set_entry_point("writer")
graph_builder.add_edge("writer", "human_edit")
graph_builder.add_conditional_edges("human_edit",
                                    route_after_interrupt,
                                    {
                                        "continue": "writer",
                                        "end": END,
                                    })

graph_form = graph_builder.compile()
