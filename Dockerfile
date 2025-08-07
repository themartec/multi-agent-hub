FROM langchain/langgraph-api:3.11



# -- Adding local package . --
ADD . /deps/multi-agent-hub
# -- End of local package . --

# -- Installing all local dependencies --
RUN PYTHONDONTWRITEBYTECODE=1 pip install --no-cache-dir -c /api/constraints.txt -e /deps/*
# -- End of local dependencies install --
ENV LANGSERVE_GRAPHS='{"react_agent": "/deps/multi-agent-hub/app/workflows/react_agent/agent.py:graph", "employer_branding_mvp": "/deps/multi-agent-hub/app/workflows/employer_branding_mvp/agent.py:workflow", "eb_form": "/deps/multi-agent-hub/app/workflows/eb_form_chat/main_graph.py:graph_form", "employer_branding_company": "/deps/multi-agent-hub/app/workflows/employer_branding_company/agent.py:workflow", "chat_agent_ec2": "/deps/multi-agent-hub/app/workflows/chat_agent_ec2/agent.py:workflow_ec2"}'



# -- Ensure user deps didn't inadvertently overwrite langgraph-api
RUN mkdir -p /api/langgraph_api /api/langgraph_runtime /api/langgraph_license &&     touch /api/langgraph_api/__init__.py /api/langgraph_runtime/__init__.py /api/langgraph_license/__init__.py
RUN PYTHONDONTWRITEBYTECODE=1 pip install --no-cache-dir --no-deps -e /api
# -- End of ensuring user deps didn't inadvertently overwrite langgraph-api --
# -- Removing pip from the final image ~<:===~~~ --
RUN pip uninstall -y pip setuptools wheel &&     rm -rf /usr/local/lib/python*/site-packages/pip* /usr/local/lib/python*/site-packages/setuptools* /usr/local/lib/python*/site-packages/wheel* &&     find /usr/local/bin -name "pip*" -delete
# -- End of pip removal --

WORKDIR /deps/multi-agent-hub