import csv

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from app.schemas.models import OpenAIModelName

system_prompt_template = """You are an admin of Employee Branding team \
You are interacting with a Content Creator\

{instructions} \

When you're all done, respond with single word 'DONE' only.
"""


def _swap_roles(messages):
    new_messages = []
    for m in messages:
        if isinstance(m, AIMessage):
            new_messages.append(HumanMessage(content=m.content))
        else:
            new_messages.append(AIMessage(content=m.content))
    return new_messages


def simulated_user_node(state):
    messages = state["messages"]
    new_messages = _swap_roles(messages)

    system_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt_template),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )
    instructions = ""
    testcase_source = "app/workflows/employer_branding_mvp/test/testcase.csv"
    with open(testcase_source, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            instructions = row['Prompt']
            break
    simulated_user = system_prompt.partial(name="Harrison Johny", instructions=instructions) | ChatOpenAI(
        model=OpenAIModelName.GPT_41, temperature=0.5, max_tokens=500)
    response = simulated_user.invoke({"messages": new_messages})
    return {"messages": [HumanMessage(content=response.content)]}
