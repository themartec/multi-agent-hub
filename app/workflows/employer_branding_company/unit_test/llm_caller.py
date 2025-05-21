from langsmith import wrappers
from openai import OpenAI
from langsmith import Client
from app.workflows.employer_branding_company.unit_test.dataset import get_example
from app.workflows.employer_branding_company.unit_test.evaluator import instruction_evaluator
from app.workflows.employer_branding_company.utils.system_prompts import get_agent_system_message

# Wrap the OpenAI client for LangSmith tracing
openai_client = wrappers.wrap_openai(OpenAI())


# Define the application logic you want to evaluate inside a target function
# The SDK will automatically send the inputs from the dataset to your target function
def target(inputs: dict) -> dict:
    response = openai_client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": get_agent_system_message("employer_branding_mvp_plus")},
            {"role": "user", "content": inputs["question"]},
        ],
    )
    return {"answer": response.choices[0].message.content.strip()}


client = Client()
dataset_name = "Automation Test Dataset"

# dataset = client.create_dataset(
#     dataset_name=dataset_name, description="Test Dataset"
# )
testcase_generate_dir = "app/workflows/employer_branding_company/unit_test/testcase_unit_generate.csv"
testcase_transform_dir = "app/workflows/employer_branding_company/unit_test/testcase_unit_transform.csv"
# # Add examples to the dataset
# dataset_id = dataset.id
client.create_examples(dataset_id="b92acce9-dd90-413c-8dbf-8a039065ea70", examples=get_example(testcase_transform_dir))

# After running the evaluation, a link will be provided to view the results in langsmith
experiment_results = client.evaluate(
    target,
    data=dataset_name,
    evaluators=[
        instruction_evaluator,
        # can add multiple evaluators here
    ],
    experiment_prefix="test-mvp-transform",
    max_concurrency=2,
)
