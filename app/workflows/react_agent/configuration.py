## Using Pydantic
from pydantic import BaseModel, Field
from typing import Annotated, Literal, Optional

from langchain_core.runnables import RunnableConfig, ensure_config

class Configuration(BaseModel):
    """The configuration for the agent."""

    system_prompt: str = Field(
        default="You are a helpful AI assistant.",
        description="The system prompt to use for the agent's interactions. "
        "This prompt sets the context and behavior for the agent.",
        json_schema_extra={
            "langgraph_nodes": ["call_model"],
            "langgraph_type": "prompt",
        },
    )

    model: Annotated[
        Literal[
            "gpt-4o-mini",
            "o1-mini",
            "o3-mini",
            "gpt-4o",
            "gpt-4.1",
        ],
        {"__template_metadata__": {"kind": "llm"}},
    ] = Field(
        default="gpt-4o-mini",
        description="The name of the language model to use for the agent's main interactions. "
        "Should be in the form: provider/model-name.",
        json_schema_extra={"langgraph_nodes": ["call_model"]},
    )
    
    @classmethod
    def from_runnable_config(
        cls, config: Optional[RunnableConfig] = None
    ) -> "Configuration":
        """Create a Configuration instance from a RunnableConfig object."""
        config_dict = ensure_config(config)
        configurable = config_dict.get("configurable") or {}
        return cls(**{k: v for k, v in configurable.items() if k in cls.model_fields})