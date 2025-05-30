task_descriptions_dict = {
    "find": {
        "Content for a Job Ad": """Identify existing content from the Library (videos, blog posts, quotes, etc.) that enhances or supports a specific job ad.

AI should scan for assets that highlight team culture, values, growth stories, or role-specific insights—anything that can emotionally connect with potential candidates.""",
        "Highlight reels from Video": """Surface short-form content snippets (clips or quotes) that are relevant to a specific topic, job, or EVP theme.""",
        "Social quotes": """Surface short-form content snippets (clips or quotes) that are relevant to a specific topic, job, or EVP theme."""
    }
}

task_instructions_dict = {
    "find": {
        "Content for a Job Ad": """Scan the job details provided by users.

Use get_library_content tool.

Output includes:

2–3 content suggestions with title/type/summary

For each, include a short sentence on why it fits (e.g. “Shows what it’s like to work on this team”)

Best practices:

Prioritize employee stories, team spotlights, or EVP-aligned content

Match by role, department, value, or job theme (e.g., flexibility, tech challenge, early career)

Avoid generic matches—look for content that adds context to the job""",
        "Highlight reels from Video": """User provides: Topic or use-case (e.g., “Belonging in tech,” “Remote work experience,” “Why I joined the company”)

Use get_content_from_library tool to perform this serch.

Elaborate from the user's provided topic to create the search keyword. For example, if the topic is remote wor

Only search among Video content

Output includes:

2–4 content pieces (as direct quotes). Each quotes should include 2-3 sentences that highlight the most important parts of the content.

Add metadata if available: speaker name, team, video title, transcript timestamp

For each, explain why it’s relevant to the request

Best practices:

Prioritize strong emotion, insight, or a memorable turn of phrase

For video, provide a summary and clip timestamp if applicable""",
        "Social quotes": """User provides: Topic or use-case (e.g., “Belonging in tech,” “Remote work experience,” “Why I joined the company”)

Output includes:

2–4 content pieces (as direct quotes). Each quotes should include 2-3 sentences that highlight the most important parts of the content.

Add metadata if available: speaker name, team, video title, transcript timestamp

For each, explain why it’s relevant to the request

Best practices:

Prioritize strong emotion, insight, or a memorable turn of phrase

For video, provide a summary and clip timestamp if applicable"""
    }
}