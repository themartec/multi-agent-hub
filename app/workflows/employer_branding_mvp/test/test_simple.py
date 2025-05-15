import csv
import logging
import sys

from langchain_core.messages import ToolMessage, AIMessage, HumanMessage
from langgraph.constants import END
from langgraph.graph import StateGraph, MessagesState

from app.workflows.employer_branding_mvp.agent import workflow
from app.workflows.employer_branding_mvp.test.simulated_user import simulated_user_node
from app.workflows.employer_branding_mvp.test.testcase import test_case_list
from app.workflows.react_agent.configuration import Configuration

logging.basicConfig(filename='log.txt', level=logging.INFO)


def _should_continue_user(state):
    messages_input = state["messages"]
    last_message = messages_input[-1]
    if len(messages_input) > 5:
        return "end"

    if last_message.content.strip().upper() == "DONE":
        print("We reach FINISHED")
        return END

    if isinstance(last_message, ToolMessage):
        return "continue"

    if isinstance(last_message, AIMessage):
        return "continue"

    return "continue"


def post_chatbot_routing(state: MessagesState):
    last = state["messages"][-1]
    second_las = state["messages"][-2]
    # # Case 1: Tool was just called — go to tool next
    # if isinstance(last, AIMessage) and last.tool_calls:
    #     return "tools"
    #
    # # Case 2: Tool result just received — go to user
    # if isinstance(last, ToolMessage):
    #     return "chatbot"  # back to bot to process result
    if isinstance(second_las, HumanMessage) and "DONE" in second_las.content.strip().upper():
        return "end"
    if isinstance(last, AIMessage):
        return "user_agent"

    return "end"


def graph_chatbot_node(state):
    result = workflow.invoke({"messages": state["messages"][-1]})
    return {**state, **result}


def call_graph():
    print("Start the Graph !")
    workflow = StateGraph(MessagesState, config_schema=Configuration)
    workflow.add_node("user_agent", simulated_user_node)
    workflow.add_node("chatbot", graph_chatbot_node)
    workflow.set_entry_point("user_agent")
    workflow.add_edge("user_agent", "chatbot")
    # Edge definition
    workflow.add_conditional_edges(
        "user_agent",
        _should_continue_user,
        {
            "continue": "chatbot",
            "end": END,
        },
    )
    workflow.add_conditional_edges("chatbot",
                                   post_chatbot_routing, {
                                       "user_agent": "user_agent",
                                       "end": END,
                                   })

    # graph = workflow.compile()
    # for chunk in graph.stream({"messages": []}):
    #     # Print out all events aside from the final end chunk
    #     if END not in chunk:
    #         # print(chunk)
    #         if 'chatbot' in chunk:
    #             chat_data = chunk.get("chatbot", {})
    #             for message in chat_data['messages']:
    #                 if isinstance(message, ToolMessage):
    #                     tool_data = message.content
    #                     print(f"**Tools**:\n{tool_data}")
    #                 if isinstance(message, AIMessage) and message.content:
    #                     print(f"**ChatBot**:\n{message.content}")
    #             print("-------------------------------------------")
    #         else:
    #             chat_data = chunk.get("user_agent", {})
    #             messages = chat_data.get("messages", [])
    #             # role = 'user_agent'
    #             content = messages[0].content
    #             print(f"**User**:\n{content}")
    #             print("-------------------------------------------")


# testcase_dir = "app/workflows/employer_branding_mvp/test/testcase.csv"
# with open('log.txt', 'w') as f:
#     sys.stdout = f
#     for testcase in test_case_list:
#         data = [['Prompt'], [str(testcase)]]
#         with open(testcase_dir, 'w', newline='') as csvfile:
#             writer = csv.writer(csvfile, delimiter=',')
#             writer.writerows(data)
#
#         call_graph()
#
#         with open(testcase_dir, 'w', newline='') as csvfile:
#             writer = csv.writer(csvfile, delimiter=',')
#             writer.writerows([])
