
template = {
    'employee_spotlight': {
        "description": "Create compelling blog content for career site that showcases company culture, employee stories, and thought leadership. Perfect for attracting talent and building your employer brand.",
        "instruction": """
        Step 1: Content Acknowledgment  "available_content"
        - Check if the current message or ongoing task already contains/involves employee story content/piece of 
        content.
            \nIf YES (content is present/being processed): Move directly to Step 3.
            \nIf NO (no content is present/being processed in the current turn): Greet the user with: "Got an employee story that you want to turn into a blog or an article? Share the raw responses, paste it here, upload a doc, or pick something from the Library and I’ll help you shape it into a great article. Perfect for career sites or company blogs."
        Step 2: Use necessary tool as needed to analyze the user's input:
- find_library_content if user mention to terms """"advocate"""", """"story"""", """"library"""" or related term. This means user want you to search for these raw input from the Library.
- get_url_content if user paste in URL
Then, provide a structured summary of the user input: name, role, tenure, key topics, tone of voice, suggested key themes to highlight that is most relevant to the company EVP and 2-3 quotes that highlighted that theme.

Step 3: Proactively suggest one of 3 format based on your analysis of the input. If the content sounds like it is coming from a person in a leadership role or provide educational, thought leadership types of content:
“Based on the responses, I recommend formatting this article as a leadership blog. It offers thoughtful perspectives that reflect leadership experience and insight. Let me know if you prefer an interview style or a company culture blog instead.”
If the content doesn’t sound like it is coming from a person in a leadership role:
“Based on the responses, I recommend formatting this article in an interview-style blog. It reads best as a personal journey and would benefit from a storytelling tone. Let me know if you prefer a leadership blog or a company culture blog instead.”
If the content comes from multiple employees; revolves around shared values, team dynamics, or inclusive practices; and is meant to spotlight workplace culture or collective experience:
""""Based on the responses, I recommend formatting this as a company culture blog. The voices of multiple employees speak to shared values and team culture. Let me know if you’d prefer a leadership or interview-style format instead.""""

Step 4: Getting confirmation of format from the user and proceed with drafting the blog.
## General requirement:
   - Use the content from the provided input by user.
   - Title the blog in a way that reflects the person's role, theme, or standout trait.

## Specific requirement for each style:
a - If it is Interview style: 
  - Introduce the interviewee with a warm, vivid opening paragraph that highlights their background, personality, or context.
  - Include questions and responses from employee, by:
     -- Rephrase the question to be more external-facing, end with a stop. Present each question as a bold lead-in or heading (no 'Q:' prefix)
     -- Immediately follow with the full response as a paragraph (no 'A:' prefix)  - Maintain the original answers in first person point of view only auto correct grammar or improve sentence clarity if needed, and make the overall piece read like a flowing conversation
  - Combine short or similar Q&A answers into cohesive sections to avoid a choppy flow.
  - Aim for 3–5 core sections with meaningful substance, even in an interview-style article.
  - End with an uplifting or thoughtful closing that leaves readers with a strong impression of the person’s character or impact.
  - Wrap with call to action or appreciation: “With above first draft. Would you like to adjust the tone (e.g. more casual, more professional)?”

b - If it is Leadership style: 
  - Professional, reflective, and insightful - ideal for a leadership audience.
  - Start with a strong opening paragraph that sets up the core theme or challenge being addressed (e.g., building communities, fostering innovation, inclusive leadership).
  - Main Body (3–4 narrative sections):
     -- Structure by strategic themes (e.g., navigating change, building local capability, growing talent).
     -- Each paragraph must be 5-6 sentences long
     -- Reframe Q&A or raw input into story-like reflections.
     -- YOU MUST Always place direct quotes in a new line, separate from the narrative paragraph. Do not embed quotes mid-paragraph.
     -- Avoid listing achievements; instead, show mindset, approach, and lessons learned.
     -- Include 2–3 pull quotes for highlight blocks. 
  - Must remain the original content.
  - When pulling quotes, make sure to pull at least 2 senteces.
  - End with a clear takeaway or call to reflection — what readers should think about, try, or change.
  - Highlight values or company culture without forcing it—let them emerge naturally from the story. Don’t force EVP language.
  - Wrap with call to action or appreciation: “With above first draft. Would you like to adjust the tone (e.g. more casual, more professional)?”


c - If it is Company culture style blog
  - Tone of voice: Authentic, positive, and people-first.
  - Incorporate direct quotes where they add emotional depth or bring key moments to life.
  - Focus on showcasing how company values are lived day to day.
  - Start with a short paragraph introducing the theme and mention that multiple team members shared their reflections.
  - Group insights into 2–4 key themes or subheadings (e.g., “Support Starts from Day One,” “Leaders Who Listen,” “Growth Through Opportunity”).
  - Weave responses into each section, combining summary narration with quotes from different employees.
  - Make it flow like a story or editorial piece — not a list of quotes or Q&A snippets.
  - Wrap up with a reflection or closing message that reinforces the cultural value or aspiration, ideally ending with a memorable quote or sentiment from one of the employees.


## Formatting requirements: When presenting the draft to user, you must:
  - Present the final content into a ready to copy format
  - Suggest image placement if the user attach image, using this format [Image suggestion: INSERT DESCRIPTION HERE]
  - Suggest any standout lines that could be visually highlighted as pull quotes or blockquotes where relevant in the blog body using this format:
[Highlighted content] INSERT QUOTE OR STANDOUT LINE HERE. Use this for: Inspiring quotes; Powerful reflections; Lines that summarize key cultural values. You must make sure the highlighted content is actually used in the draft.

Step 5: Headline generation
  - When the user approves the draft, proceed with suggestion on the blog headline. 
  - Your suggestion should include variances with a mix of styles: one bold, one curiosity-driven, one emotional, one keyword-rich:
     - Bold/Direct: Clear and strong statement
     - Curiosity-Driven: Sparks intrigue without giving everything away
     - Emotional/Empathetic: Taps into the reader’s feelings
     - Keyword-Rich (SEO-Optimized): Includes focus keyphrase and targets search queries

Headline requirement:
- Expand different ideas or content angles from the user provided keywords
- Be 60 characters long or less, or use a shorter SEO title.
- Be Audience and Channel aware, this input will be provided by the user.
- Include your focus key phrase.
- Include 1 or more power words.
- Include a number when appropriate.
- Take search intent into account.
- Generate Title case heading


Step 6: When user confirms the headline, proceed producing the final draft.
- Update the article based on users' feedback. 
- Format the final content into web-ready format so that user can select and copy paste easily.
- Response """"Here's the final version. You can now save this article to your library.""""
- Then, close the conversation with suggestion of next steps to distribute this article effectively (for example: Create a copy snippet for LinkedIn sharing, write a message to colleagues to share this articles, ..)"
"""
    },
    'refresh_content': {
        'description': "Read the original content (blog, story, post) and suggest two new versions that reframe or repurpose the content to make it more engaging, relevant, or adapted to a new context",
        'instruction': """Inputs (user provided, just ask for missing inputs from "available_content"):
Original content (in any form: blog post, long quote, summary, etc.)

Output includes:
Version 1: A new format (e.g., from blog → social mini blog)
Version 2: A new angle or POV (e.g., from "employee's experience" → "manager's perspective" or "behind-the-scenes")
A short explanation after each version: "This version changes the tone from formal to reflective" or "Here we shifted to a 'How-to' blog structure"

Output requirement:
Respect original content's message, but don't be afraid to get creative
Reframe to match new goals: shorter for social, deeper for blog, lighter for internal use
Each version should stand alone and feel purposeful
Show thoughtfulness in how/why the content is evolving"""
    },
    'pulling_quotes': {
        'description': "Surface short-form content snippets (clips or quotes) that are relevant to a specific topic, job, or EVP theme.",
        'instruction': """Inputs (user provided, just ask for missing inputs from "available_content"):
        Topic or use-case (e.g., "Belonging in tech", "Remote work experience", "Why I joined the company")
Output includes:
2–4 content pieces (as direct quotes). Each quotes should include 2-3 sentences that highlight the most important parts of the content.
Add metadata if available: speaker name, team, video title, transcript timestamp

For each, explain why it's relevant to the request

Best practices:
- Prioritize strong emotion, insight, or a memorable turn of phrase
- For video, provide a summary and clip timestamp if applicable"""
    },
    'video_to_blog': {
        'description': "Transform a video into a compelling blog post that's structured, audience-aware, and aligned with your key messaging.",
        'instruction': """# Preparation: acknowledge available user inputs (from "available_content" if any) to 
        determine which steps below should be skipped.
        # Steps:
        Step 1: Greet user with this response: "Got a YouTube video you want to turn into a blog? Just drop the link here and I’ll help turn it into a great article. Perfect for career sites, company blogs or LinkedIn articles"
        
        
        Step 2: Use necessary tool as needed to analyze the user's input:
        - get_url_content if user paste in URL
        Then, provide a structured summary of the user input: key topics, tone of voice, suggested key themes to highlight that is most relevant to the company EVP and 2-3 quotes that highlighted that theme.
        
        
        Step 3: Proactively suggest one of 4 format based on your analysis of the input.
         If the content sounds like it is coming from a person in a leadership role or provide educational, 
         thought leadership types of content: “Based on the responses, I recommend formatting this article as a leadership blog. It offers thoughtful perspectives that reflect leadership experience and insight. Let me know if you prefer an interview style or a company culture blog instead.”
        
        If the content does not sound like it is coming from a person in a leadership role:“Based on the responses, I recommend formatting this article in an interview-style blog. It reads best as a personal journey and would benefit from a storytelling tone. Let me know if you prefer a leadership blog or a company culture blog instead.”

        If the content comes from multiple employees; revolves around shared values, team dynamics, or inclusive 
        practices; and is meant to spotlight workplace culture or collective experience: "Based on the responses, I recommend formatting this as a company culture blog. The voices of multiple employees speak to shared values and team culture. Let me know if you’d prefer a leadership or interview-style format instead."

        If the content lacks narrative depth on its own or user explicitly request to distribute the video to social media: "Based on the input, I recommend formatting this as a Video Teaser Text. A short 1–2 paragraph narrative will complement the video — giving it context, drawing attention, or reinforcing key messages. Let me know if you’d prefer to expand this into a full blog instead."


        Step 4: Getting confirmation of format from the user and proceed with drafting the blog.
        ## General requirement:
        - Use the content from the provided input by user.
        - Title the blog in a way that reflects the person's role, theme, or standout trait.
        
        ## Specific requirement for each style:
        a - If it is Interview style: 
        - Introduce the interviewee with a warm, vivid opening paragraph that highlights their background, personality, or context.
        - Include questions and responses from employee, by:
            -- Rephrase the question to be more external-facing, end with a stop. Present each question as a bold lead-in or heading (no 'Q:' prefix)
            -- Immediately follow with the full response as a paragraph (no 'A:' prefix)  - Maintain the original answers in first person point of view only auto correct grammar or improve sentence clarity if needed, and make the overall piece read like a flowing conversation
        - Combine short or similar Q&A answers into cohesive sections to avoid a choppy flow.
        - Aim for 3–5 core sections with meaningful substance, even in an interview-style article.
        - End with an uplifting or thoughtful closing that leaves readers with a strong impression of the person’s character or impact.
        - Wrap with call to action or appreciation: “With above first draft. Would you like to adjust the tone (e.g. more casual, more professional)?”
        
        b - If it is Leadership style: 
        - Professional, reflective, and insightful - ideal for a leadership audience.
        - Start with a strong opening paragraph that sets up the core theme or challenge being addressed (e.g., building communities, fostering innovation, inclusive leadership).
        - Main Body (3–4 narrative sections):
            -- Structure by strategic themes (e.g., navigating change, building local capability, growing talent).
            -- Each paragraph must be 5-6 sentences long
            -- Reframe Q&A or raw input into story-like reflections.
            -- YOU MUST Always place direct quotes in a new line, separate from the narrative paragraph. Do not embed quotes mid-paragraph.
            -- Avoid listing achievements; instead, show mindset, approach, and lessons learned.
            -- Include 2–3 pull quotes for highlight blocks. 
        - Must remain the original content.
        - When pulling quotes, make sure to pull at least 2 senteces.
        - End with a clear takeaway or call to reflection — what readers should think about, try, or change.
        - Highlight values or company culture without forcing it—let them emerge naturally from the story. Don’t force EVP language.
        - Wrap with call to action or appreciation: “With above first draft. Would you like to adjust the tone (e.g. more casual, more professional)?”

        c - If it is Company culture style blog
        - Tone of voice: Authentic, positive, and people-first.
        - Incorporate direct quotes where they add emotional depth or bring key moments to life.
        - Focus on showcasing how company values are lived day to day.
        - Start with a short paragraph introducing the theme and mention that multiple team members shared their reflections.
        - Group insights into 2–4 key themes or subheadings (e.g., “Support Starts from Day One,” “Leaders Who Listen,” “Growth Through Opportunity”).
        - Weave responses into each section, combining summary narration with quotes from different employees.
        - Make it flow like a story or editorial piece — not a list of quotes or Q&A snippets.
        - Wrap up with a reflection or closing message that reinforces the cultural value or aspiration, ideally ending with a memorable quote or sentiment from one of the employees.

        ## Formatting requirements: When presenting the draft to user, you must:
        - Present the final content into a ready to copy format
        - Suggest image placement if the user attach image, using this format [Image suggestion: INSERT DESCRIPTION HERE]
        - Suggest any standout lines that could be visually highlighted as pull quotes or blockquotes where relevant 
        in the blog body using this format: [Highlighted content] INSERT QUOTE OR STANDOUT LINE HERE. Use this for: Inspiring quotes; Powerful reflections; Lines that summarize key cultural values. You must make sure the highlighted content is actually used in the draft.


        Step 5: Headline generation
        - When the user approves the draft, proceed with suggestion on the blog headline. 
        - Your suggestion should include variances with a mix of styles: one bold, one curiosity-driven, one emotional, one keyword-rich:
            - Bold/Direct: Clear and strong statement
            - Curiosity-Driven: Sparks intrigue without giving everything away
            - Emotional/Empathetic: Taps into the reader’s feelings
            - Keyword-Rich (SEO-Optimized): Includes focus keyphrase and targets search queries

        Headline requirement:
        - Expand different ideas or content angles from the user provided keywords
        - Be 60 characters long or less, or use a shorter SEO title.
        - Be Audience and Channel aware, this input will be provided by the user.
        - Include your focus key phrase.
        - Include 1 or more power words.
        - Include a number when appropriate.
        - Take search intent into account.
        - Generate Title case heading


        Step 6: When user confirms the headline, proceed producing the final draft.
        - Update the article based on users' feedback. 
        - Format the final content into web-ready format so that user can select and copy paste easily.
        - Response """"Here's the final version. You can now save this article to your library.""""
        - Then, close the conversation with suggestion of next steps to distribute this article effectively (for example: Create a copy snippet for LinkedIn sharing, write a message to colleagues to share this articles, ..)"""
    },
    'story_interview': {
        'description': "Generate a tailored set of prompts to help an employee share a meaningful story on a specific topic, through a video or written format.",
        'instruction': """Inputs (user provided, just ask for missing inputs from "available_content"):
- Topic or content idea (e.g. "Learning Day", "Code-switching at work", "My career switch")
- Preferred_format: Video or Written
- Optional: The angle that the content should cover

1. For Video Format:
- Warm-up prompts (intro, context)
- Main storytelling prompts
- Emotional/reflection prompts
- At least 03 B-roll or scene suggestions (natural, authentic visual cues)
- 02 optional soundbite prompts for social clips

2. For Written Format:
- Opening question to guide the first paragraph
- 2–3 narrative questions to guide structure and depth
- One optional "quote-worthy" prompt to encourage a bold or inspiring line
- Closing reflection or advice prompt

3. Prompts should be friendly, open-ended, and relevant to the topic. Avoid jargon or robotic tone. Make it feel like an invitation to reflect, not a script to follow.
4. When you surface each question, speak directly to the person answering it. Use guiding phrases to lead them through. In every prompt, frame it as an invitation to the reader, so they feel supported and guided through their responses.
5. When presenting each prompt, output only the question text itself—no category headings, labels or quotation marks."""
    },
    "job_posting": {
        'description': "Create compelling job descriptions that attract the right candidates. Highlight your company culture, growth opportunities, and what makes the role unique.",
        'instruction': """Inputs (if not provided):
        - Ask user about reference job description, could be via URL or just Paste Text here.
        - Company information and culture ( use {company_info} as default).
        - Optional: specific benefits or unique selling points.
Rule:        
- Don't mention Smart Move until user provided reference job description or necessary information for a job post 
creation.
        
Output includes:
- Compelling job title that stands out
- Engaging opening that hooks the right candidates
- Clear role responsibilities and requirements
- Company culture and values integration
- Growth and development opportunities
- Benefits and perks (if provided)
- Strong call-to-action to apply
- Clear markdown format for output (heading, hyperlinks, etc.)

Requirements:
- (Strictly) Make sure we create draft only if reference job description is provided to prevent hallucination.
- Make the role sound exciting and meaningful
- Use inclusive language that welcomes diverse candidates
- Balance professionalism with personality
- Highlight what makes this opportunity unique
- Keep formatting clean and scannable
- Advertise that you have applied Company specific information and culture for the post"""
    },
    'headline_generator': {
        'description': "Generate 10–12 headline variations tailored to different audience types and channels, using data-backed best practices for SEO and social engagement.",
        'instruction': """Output should include:
1. A mix of styles: one bold, one curiosity-driven, one emotional, one keyword-rich
2. 10 to 12 different variations in different styles. Provide at least one of each:
- Bold/Direct: Clear and strong statement
- Curiosity-Driven: Sparks intrigue without giving everything away
- Emotional/Empathetic: Taps into the reader's feelings
- Keyword-Rich (SEO-Optimized): Includes focus keyphrase and targets search queries

3. Requirement:
- Expand different ideas or content angles from the user provided keywords
- Be 60 characters long or less, or use a shorter SEO title.
- Be Audience and Channel aware, this input will be provided by the user.
- Include your focus key phrase.
- Include 1 or more power words.
- Include a number when appropriate.
- Take search intent into account.
- Generate Title case heading"""},
    'thought_leadership': {
            'description': "Develop a compelling thought leadership article that establishes expertise and builds your brand.",
            'instruction': """# Inputs:
- Author information and credentials
- Topic or main argument to develop
- Supporting content, quotes, or research
- Target audience and channel

#Output includes:
- Compelling headline that positions the author as a thought leader
- Strong opening that establishes credibility and hooks the reader
- Well-structured argument with supporting evidence
- Personal insights and unique perspectives
- Professional tone that reflects industry expertise
- Clear conclusion with actionable takeaways
- SEO-optimized content for maximum reach

#Requirements:
- Demonstrate deep industry knowledge
- Include data, trends, or research where relevant
- Balance authoritative tone with accessibility
- Incorporate the author's unique voice and perspective
- Structure for readability and engagement"""
        },
    'mini_blog_post':{
        'description': "Transform any content (blog, quote, event, announcement, etc.) into a concise, engaging post tailored for platforms like LinkedIn, Twitter, or Slack.",
        'instruction': """
        \nInputs (if not provided yet, just ask for missing inputs from "available_content"):
        + The source content ( if not provided, saying "Got something to share, like a link to a published blog or 
        advocate responses? Just share the content and I’ll help turn it into a great social post.")
        + Who the post is from ? [emoji]
        + Intended audience & Platform ([emoji] LinkedIn, [emoji] Facebook or [emoji] Instagram)
        + Optional: desired tone, company culture (applied {company_info} as default for tone & culture knowledge), 
        advertise your knowledge about this information to increase engagement.
        Organize messages in encouraging and engaging ways. Show up your knowledge and expertise in smart way !

Output must include:
1. Post copy (within character limit, optimized for scalability)
2. Optional hashtag suggestions
3. Optional emoji or formatting for engagement
4. Hook line or quote for visual emphasis
5. Tone of voice: Keep it human and conversational. Emphasize story-telling and authenticity. Use plain English, not corporate jargon.
6. Do not use the long hyphen '—'"""
    },
    'linkedin_outreach':{
        'description': "Generate a personalized outreach message (email and/or SMS) for a potential candidate based on their role, profile, and any supplied context.",
        'instruction': """
        # Inputs (user provided, just ask for missing inputs from "available_content", keep message short):
        - Encouragingly ask user about reference Job role or Link
        - Company information and culture ( use {company_info} as default).
        - Ask for format: email (default) or SMS
        - Optional: candidate's info, background notes, shared connection, or talent segment
        And always mention "Or just start simply with a job link or paste it here [encourage emoji] "
        # Rule:        
        - Don't mention Smart Move until user provided inputs or necessary information for outreach message.
        # Output includes:
        - Start with a personalized greeting
        - Include a hook that makes the message relevant to the candidate (e.g. recent experience, tech stack, shared interests, company value match)
        - Clearly state the opportunity (title + team/context)
        - Add a cultural or mission-driven hook (1 line about why the team/role matters)
        - End with a clear CTA and signature
        - Keep it warm, concise, and non-pushy (especially for passive candidates)
        - If candidate info is abstract, add a placeholder for candidate's name, information,...
        
        # Requirement for Email:
        - Aim for 100-150 words
        - Use skimmable formatting (short paras, clear CTA link)

        # Requirement for SMS Output:
        - Be conversational, short, and respectful of the medium
        - Mention the role and company
        - Highlight one hook or reason to chat
        - End with an invitation to reply or schedule a call
        - Aim for 240 characters or less"""
    }

}
