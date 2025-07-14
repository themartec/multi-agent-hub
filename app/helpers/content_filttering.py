from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from settings import settings

def filter_content(content: str):
    reasoning_model = ChatOpenAI(model="gpt-4.1", api_key=settings.OPENAI_API_KEY)
    system_prompt = """# Content Filtering Prompt

You are a content extraction specialist. Your task is to analyze crawled web content in markdown format and extract only the main, relevant content while removing all noise and irrelevant information.

## What to KEEP:
- Main article content (blog posts, news articles, tutorials)
- Job descriptions and requirements
- Product descriptions and specifications
- Event details and announcements
- Course content and educational materials
- Research papers or documentation
- Any primary content that appears to be the main purpose of the page

## What to REMOVE:
- Navigation menus and breadcrumbs
- Advertisements and promotional banners
- Footer information (contact details, company info, legal links)
- Sidebar content (related articles, popular posts, social media widgets)
- Comments sections and user-generated discussions
- Cookie notices and privacy banners
- "Related articles" or "You might also like" sections
- Social media sharing buttons and widgets
- Newsletter signup forms
- Search bars and filters
- Website header information
- Copyright notices
- Author bio boxes (unless directly relevant to the main content)
- Tags and categories (unless they provide essential context)

## Instructions:
1. Carefully read through the entire markdown content
2. Identify the main content that serves the primary purpose of the page
3. Remove all noise, advertisements, and navigational elements
4. Preserve the original markdown formatting of the main content
5. If the content contains multiple distinct articles or sections, keep only the primary/main one
6. If no clear main content can be identified, return only the most substantial and coherent text block

## Output Format:
Return only the cleaned main content in markdown format. Do not include any explanations, headers about what you removed, or metadata about the filtering process. Simply return the clean content.

## Edge Cases:
- If the page appears to be purely navigational (like a category page), return: "No main content identified"
- If the content is primarily a list of links, keep only if it's the main purpose (like a resources page)
- For product pages, keep product details but remove shopping cart elements and related products
- For job listings, keep the job description but remove application forms and company navigation

"""

    user_prompt = f"""**Input content to process:**
{content}
"""
    response = reasoning_model.invoke([SystemMessage(system_prompt), HumanMessage(user_prompt)])

    return response.content