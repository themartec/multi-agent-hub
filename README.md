# Multi-agent Hub
Author: *Le Tan Nghia (Jack Nghia)*

# Dev Development
1. Create a .env file in environment folder following the .env.example and fill in the missing values:
- For OPENAI_API_KEY, get it in https://platform.openai.com/api-keys
- For JINA_API_KEY, get it in https://jina.ai/api-dashboard/key-manager
- For LANGSMITH_API_KEY, get it in settings of smith.langchain.com
- For AUTHEN_TOKEN, get it in uat platform
2. Create virtual env:
```bash
conda create -n agent-hub python=3.12
conda activate agent-hub
pip install -e .
```
3. Run langgraph dev server
```bash
langgraph dev
```