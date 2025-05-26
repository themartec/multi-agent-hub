from openevals.llm import create_llm_as_judge
from pydantic import BaseModel

INSTRUCTION_PROMPT = """You are an experience editor who take care for quality of content.
Your task is to check the quality of instruction alignment of output following the rubric below.

<Rubric>
instruction_alignment will be:
- Good: if output is aligned with instruction completely
- Acceptable: if output is aligned with instruction partially
- Bad: if output is not aligned with instruction
</Rubric>

<Instructions>
Please carefully check each factor of input like task description (generate Employee story or Team story,...), 
detail instruction, topic, tone, audience, and so on...
It is good if you justification/reasoning mention case by case as bullet point to review
</Instructions>

Please label for feedback_key as instruction_alignment the following example according to the above instructions:

<input>
{inputs}
</input>

<output>
{outputs}
</output>
"""


class InstructionEvaluator(BaseModel):
    instruction_alignment: dict


def instruction_evaluator(inputs: dict, outputs: dict):
    assert outputs['answer'], f"output is empty"
    evaluator = create_llm_as_judge(
        prompt=INSTRUCTION_PROMPT,
        model="openai:gpt-4.1",
        feedback_key="instruction_alignment",
    )
    eval_result = evaluator(
        inputs=inputs['question'],
        outputs=outputs['answer'],
    )
    return eval_result
