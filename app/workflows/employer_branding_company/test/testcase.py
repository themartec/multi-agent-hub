test_case_list = [
    {
        "question": """
        Generate Employee Story that Write up Employee stories from their raw sharing from raw content as:
        Content:
        'being able to truly look at a client or Prospect and say yes we can do that on any client anywhere in the world on any subject as it relates to risk management is fantastic I always have confidence that I am one phone call away from someone that can wow those people that they can go whoa does this person know my business we've worked hard to build that expertise and created a culture that says we're all part of one team we're working together we're trying to do the right thing for the client and over the years we've been able to bring that together to a point where literally I can say without question yes we do that that's pretty cool'
        Topic: A Gallagher Employee Story From CEO Pat Gallagher
        Instruction:
        - Write in first person perspective unless explicitly instruct differently.
        - Always pull in direct quotes from Content input where relevant
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
