from langgraph.graph import StateGraph, START, END

from app.workflows.employer_branding_company.utils.nodes import (
    # get_user_info,
    call_model,
    tool_node,
    first_route,
    should_continue,
    save_to_library
)
from app.workflows.employer_branding_company.utils.state import State


graph_builder = StateGraph(State)

# graph_builder.add_node("get_user_info", get_user_info)
graph_builder.add_node("agent", call_model)
graph_builder.add_node("tools", tool_node)
graph_builder.add_node("save_to_library", save_to_library)

# graph_builder.add_edge(START, "get_user_info")
graph_builder.add_conditional_edges(
    START,
    first_route,
    {
        "yes": "agent",
        "no": "agent",
        "save_to_library": "save_to_library"
    }
)
graph_builder.set_entry_point("agent")
# graph_builder.add_edge("get_user_info", "agent")
# We now add a conditional edge
graph_builder.add_conditional_edges(
    # First, we define the start node. We use `agent`.
    # This means these are the edges taken after the `agent` node is called.
    "agent",
    # Next, we pass in the function that will determine which node is called next.
    should_continue,
    # Finally we pass in a mapping.
    # The keys are strings, and the values are other nodes.
    # END is a special node marking that the graph should finish.
    # What will happen is we will call `should_continue`, and then the output of that
    # will be matched against the keys in this mapping.
    # Based on which one it matches, that node will then be called.
    {
        # If `tools`, then we call the tool node.
        "continue": "tools",
        # Otherwise we finish.
        "end": END,
    },
)

# We now add a normal edge from `tools` to `agent`.
# This means that after `tools` is called, `agent` node is called next.
graph_builder.add_edge("tools", "agent")

# Now we can compile and visualize our graph
workflow = graph_builder.compile()