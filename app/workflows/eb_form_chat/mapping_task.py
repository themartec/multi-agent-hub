from pydantic import BaseModel, Field
from typing import Literal
from langchain_openai import ChatOpenAI


from app.schemas.models import OpenAIModelName


class MapTask(BaseModel):
    task: Literal["Content Create", "Augmented Job Create", "Refinement", "Normal Support"] = Field(
        description=f"""Read through conversation list between user (human) and ai assistant (ai agent) 
        one by one orderly to determine which action should be assigned next: "Content Generation", "Augmented Job" or "Conversation".
        Consider the following rules:
        Always check latest message of ai assistant to know current context key point.
        It is important to understand whole conversation context, ex: if a draft content has been generated, 
        we don't need to map it to "Content Generation" any more.
        - if user freshly asks for content creating (ex: Generate Employee Story) map it to 'Content Create' action
        - if user freshly asks for creating a Job Description (JD) or Job Ad (JA), map it to 'Augmented Job Create' action
        - if nothing special, map it to 'Normal Support' only. 
        - if user asks for refinement or ai agent asks for refinement, map it to 'Refinement'
        The main goal of your task is to determine if we should assign so that downstream process knows what to do next
""",
    )


def mapping_task(conversion: [str]):
    print("conversion: ", conversion)
    mapping_assistant_llm = ChatOpenAI(model=OpenAIModelName.GPT_41,
                                       max_tokens=1000,
                                       temperature=0)
    mapping = mapping_assistant_llm.with_structured_output(MapTask)
    output = mapping.invoke(f"Check for conversation: {conversion}")
    return str(output.task)
