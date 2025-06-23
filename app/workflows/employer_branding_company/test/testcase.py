test_case_list = [
    {
        "question": """
        Generate Employee Story that captures a real, authentic narrative showcasing the employee’s journey, challenges,
growth, or cultural experience.
Content: https://www.gallaghersmallbusiness.com/small-business-expertise/managing-and-growing-your-business/marketing-and-customer-relations/celebrating-national-black-business-month-with-laniers-fine-candies/
Topic: Gallagher CEO sharing about the company culture
Instruction:
- Write in first person perspective unless explicitly instruct differently.
- Include direct quotes—these humanize the piece and boost authenticity.
- Make the story timeline clear: What was “before,” what changed, and what’s the takeaway?
- Highlight values or company culture without forcing it—let them emerge naturally from the story.
- Aim for emotion, relatability, and vulnerability. Let readers see themselves in the story.
- Always generate an outline and confirm with user before writing the full content""",
        "instructions": """
        - When the content creator could not scrap the content from the URL, say 'Thank you!' and end up conversation.
        - When the content creator responds your question with a outline template, say 'Yes, do it pls!'
        - When the content creator responds your question with a draft content to review, let check if that content 
        includes any quotes from the content input, if not, ask the content creator to pull in quotes from the 
        content input, if it's done, say 'Thank you!'. Otherwise, keep asking the content creator once more time 
        only.""",
    }
]
