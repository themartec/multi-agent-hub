import csv
import logging
import sys

from langchain_core.messages import ToolMessage, AIMessage, HumanMessage
from langgraph.constants import END
from langgraph.graph import StateGraph, MessagesState

from app.workflows.employer_branding_company.agent import workflow
from app.workflows.employer_branding_company.test.testcase import test_case_list
from app.workflows.employer_branding_company.test.simulated_user import simulated_user_node
from app.workflows.employer_branding_company.utils.nodes import call_model
from app.workflows.react_agent.configuration import Configuration

logging.basicConfig(filename='log_old.txt', level=logging.INFO)


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

    if isinstance(second_las, HumanMessage) and "DONE" in second_las.content.strip().upper():
        return "end"
    if isinstance(last, AIMessage):
        return "user_agent"

    return "end"


def graph_chatbot_node(state):
    result = workflow.invoke({"messages": state["messages"]})
    return {**state, **result}


def call_graph():
    print("Start the Graph !")
    workflow_test = StateGraph(MessagesState, config_schema=Configuration)
    workflow_test.add_node("user_agent", simulated_user_node)
    workflow_test.add_node("chatbot", graph_chatbot_node)
    workflow_test.set_entry_point("user_agent")
    workflow_test.add_edge("user_agent", "chatbot")
    # Edge definition
    workflow_test.add_conditional_edges(
        "user_agent",
        _should_continue_user,
        {
            "continue": "chatbot",
            "end": END,
        },
    )
    workflow_test.add_conditional_edges("chatbot",
                                   post_chatbot_routing,
                                        {
                                       "user_agent": "user_agent",
                                       "end": END,
                                   })

    graph_test = workflow_test.compile()

    for chunk in graph_test.stream({"messages": []}):
        # Print out all events aside from the final end chunk
        if END not in chunk:
            # print(chunk)
            # print("-------------------------------------------")
            if 'chatbot' in chunk:
                chat_data = chunk.get("chatbot", {})
                message = chat_data['messages'][-1]
                if isinstance(message, ToolMessage):
                    tool_data = message.content
                    print(f"**Tools**:\n{tool_data}")
                if isinstance(message, AIMessage) and message.content:
                    print(f"**ChatBot**:\n{message.content}")
                # for message in chat_data['messages']:
                #     if isinstance(message, ToolMessage):
                #         tool_data = message.content
                #         print(f"**Tools**:\n{tool_data}")
                #     if isinstance(message, AIMessage) and message.content:
                #         print(f"**ChatBot**:\n{message.content}")
                print("-------------------------------------------")
            else:
                # print(chunk)
                chat_data = chunk.get("user_agent", {})
                messages = chat_data.get("messages", [])
                # role = 'user_agent'
                content = messages[0].content
                print(f"**User**:\n{content}")
                print("-------------------------------------------")


testcase_dir = "app/workflows/employer_branding_company/test/testcase.csv"
with open('log.txt', 'w') as f:
    sys.stdout = f
    fieldnames = ['User Question', 'Simulated User Instructions']
    for testcase in test_case_list:
        question = testcase['question']
        instructions = testcase['instructions']
        data = [fieldnames,
                [question, instructions]
                ]
        with open(testcase_dir, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerows(data)

        call_graph()

        with open(testcase_dir, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerows([])
