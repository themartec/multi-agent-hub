from langgraph.graph import MessagesState
from typing import List

class State(MessagesState):
    tovs: str
    compliance_content: str
    evps: str
    first_name: str
    email: str
    company_id: str
    company_name: str
    ui: List[dict]
    english_type: str
    template_employee_spotlight: str
    template_employee_refresh_content: str
    template_pulling_quotes: str
    template_video_to_blog: str
    template_job_post: str
    template_story_interview: str
    template_linkedin_outreach: str
    template_thought_leadership: str
    template_mini_blog_post: str