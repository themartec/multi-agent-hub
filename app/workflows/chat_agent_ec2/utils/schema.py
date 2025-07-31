from pydantic import BaseModel, Field


class AgentResponse(BaseModel):
    headline: str = Field(description="Headline")
    content: str = Field(description="Body Content")