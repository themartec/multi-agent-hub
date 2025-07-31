from langgraph.graph import StateGraph, START, END

from app.workflows.chat_agent_ec2.utils.nodes import (
    get_user_info,
    call_model,
    tool_node,
    first_route,
    should_continue,
    save_to_library, init_template
)
from app.workflows.chat_agent_ec2.utils.state import State
#

graph_builder = StateGraph(State)

graph_builder.add_node("get_user_info", get_user_info)
graph_builder.add_node("init_template", init_template)
graph_builder.add_node("agent", call_model)
graph_builder.add_node("tools", tool_node)
graph_builder.add_node("save_to_library", save_to_library)

graph_builder.add_conditional_edges(
    START,
    first_route,
    {
        "yes": "get_user_info",
        "no": "agent",
        "save_to_library": "save_to_library"
    }
)
graph_builder.add_edge("get_user_info", "init_template")
graph_builder.add_edge("init_template", "agent")
graph_builder.add_conditional_edges(
    "agent",
    should_continue,
    {
        "continue": "tools",
        "end": END,
    },
)

graph_builder.add_edge("tools", "agent")

# Now we can compile and visualize our graph
workflow_ec2 = graph_builder.compile()