from pydantic import BaseModel, Field
from typing import Literal
from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState, StateGraph, END

evaluator_prompt = """
State Mapping
1. Fresh Session begin: Ask initial question likes “Are you here to plan a campaign, create a new asset, 
repurpose something existing, or distribute content that’s already ready?”
   a. If user is unsure, guide them with this prompt: “No worries! Would you like to start with a campaign theme, a story or quote, some older content to reuse, or content that’s ready to be shared?”
   And then, direct user to one of those steps: plan, create new, repurpose or distribute
2. User is required to 'repurpose': 
   a. If the inquiring is ambiguous with just a link or content name (vague input), the process of pulling data 
   should be triggered and should ask for more information "Would you like me to repurpose this for a specific 
   audience, format, or campaign goal?" and share some directions for repurposing ideas.
      a1. once user approved/agree with some ideas, it should go with a draft version & ask for refinement confirmation.
   b. If the inquiring is provided with Link/Content along with some additional information (ex: tone, audience,
   ....), it should show a draft version and ask for refinement confirmation.
Note:
   Draft version: should have
    - Adapted content pieces with audience + format labels
    - Visual notes, hashtags
    - Avoid suggest video-based content

"""


# Schema for structured output to use in evaluation
class Feedback(BaseModel):
    status: Literal["correct", "incorrect"] = Field(
        description=f"""Analyze messages history and Decide if the current step of workflow is correct or incorrect 
        as pre-definition from state mapping guideline: {evaluator_prompt}. Please match correct context to the 
        guide""",
    )
    feedback: str = Field(
        description="Your justification and If the current state of workflow is incorrect, provide note about previous "
                    "state, current state, expected state",
    )


# Augment the LLM with schema for structured output
llm_model_evaluator = ChatOpenAI(model="gpt-4o-mini", max_tokens=1000)
evaluator = llm_model_evaluator.with_structured_output(Feedback)


def llm_call_evaluator(state: MessagesState):
    eval = evaluator.invoke(f"Evaluate: {state['messages']}")
    return {"correct_or_not": eval.status, "feedback": eval.feedback}


def llm_call_evaluator_custom(conversion: []):
    assert conversion
    eval = evaluator.invoke(f"Evaluate: {str(conversion)}")
    return {"correct_or_not": eval.status, "feedback": eval.feedback}
