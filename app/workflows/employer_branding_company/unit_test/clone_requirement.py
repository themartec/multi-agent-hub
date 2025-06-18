import pandas as pd

# --- Load Excel file locally ---
csv_file_path = 'requirement_5jun2025.csv'  # Replace with the actual file path
sheet_name = 'AI Instruction'
try:
    df = pd.read_csv(csv_file_path, encoding='utf-8')
except UnicodeDecodeError:
    df = pd.read_csv(csv_file_path, encoding='windows-1252')

# --- Filter rows where Task == "Find" ---
filtered_df = df[df['Task'] != 'Find']

# --- Generate output DataFrame ---
output_df = pd.DataFrame()
output_df['Test Case'] = ""
# Test Data Input
content_written_url = "https://www.ibm.com/careers/blog/highlighting-the-success-of-women-in-tech"
content_video_url = "https://www.youtube.com/watch?v=g1UmgxcyQ0E"
content_as_raw = """Navigating the Future Together: My Journey as a Mentor at Gallagher
As the Vice President of Gallagher's Bogotá office, I have the privilege of leading a talented team and overseeing all strategic aspects of our local business. With a background in client relationship management and financial risk solutions, I joined Gallagher seven years ago, bringing with me a deep commitment to client satisfaction and operational efficiency. However, one of the most rewarding aspects of my role has been the opportunity to serve as a mentor to the next generation of leaders and professionals within our organization.
The Inspiration to Mentor
My decision to become a mentor at Gallagher stems from my own experiences with mentors who have supported my growth and helped guide me through challenges. These experiences instilled in me the importance of paying it forward and contributing to the development of others. When I joined Gallagher, I saw an opportunity to shape the future by sharing my insights and experiences with the diverse range of talent within our organization.
Mentoring has not only allowed me to help others grow, but it has also enriched my own professional journey. Engaging with fresh perspectives and innovative ideas of my mentees has challenged me to reflect on my own practices and grow alongside them, creating a dynamic and rewarding learning environment for all involved.
Tailoring the Mentoring Approach
One of the key lessons I've learned as a mentor is that a one-size-fits-all approach doesn't work. Every mentee brings their own unique strengths, challenges, and aspirations to the table. To effectively support their growth, I make it a priority to understand their individual needs and career goals through open conversations about their professional background, current challenges, and future aspirations.
Once I have a clear understanding of their objectives, I customize my guidance to align with their specific goals. This may involve providing personalized resources, setting attainable milestones, or connecting them with relevant networking opportunities. By tailoring my approach to each mentee, I can ensure that they receive the support and guidance they need to succeed.
Balancing Guidance and Autonomy
As a mentor, one of the most important aspects of my role is giving my mentees the autonomy to take ownership of their decisions empowering them to learn from their experiences. To achieve this balance, I focus on prioritizing active listening and empathy, asking open-ended questions that encourage critical thinking and self-reflection, and understanding that everyone has unique strengths and challenges.
I also emphasize the importance of learning from mistakes and reassure my mentees that it's okay to fail sometimes, as long as they are learning and growing from the experience. This approach helps build their confidence and decision-making skills over time.
Navigating Challenges Together
One of the most significant challenges I've worked through with a mentee involved navigating the balance between personal ambition and team collaboration. This particular mentee was highly driven and had great potential, but they often found themselves focusing on individual achievements at the expense of building stronger relationships within their team.
To help them overcome this challenge, I encouraged them to shift their approach by actively listening to their colleagues and seeking input from others before pushing forward with their own ideas. This experience reinforced the importance of empathy, active listening, and patience, not just as leadership skills, but as key components of successful collaboration.
The Rewards of Mentoring
Being a mentor at Gallagher has been an incredibly rewarding experience. Seeing my mentees grow, take on new challenges, and succeed in their roles is a testament to the power of mentoring and the impact it can have on an individual's career.
One memorable moment that stands out occurred when I was mentoring a colleague who was struggling with transitioning into a leadership role. By focusing on helping him navigate the softer skills required in leadership and encouraging vulnerability, I watched as he grew more comfortable in his role and his team began to respond more positively.
These experiences have shown me that small shifts in mindset can have a huge impact on someone's professional growth. Furthermore, it has taught me the importance of being open to learning from others, patient adapting to new situations, and continuously seeking ways to improve myself and my leadership style. 
To anyone considering becoming a mentor at Gallagher, my advice would be to approach the role with a genuine desire to help others grow. Keep your ears open and create an environment where your mentee feels comfortable taking risks, asking questions, and learning from both successes and failures.
As we navigate the future together at Gallagher, I am excited to continue my journey as a mentor and to see the impact that our collective efforts will have on the success of our company and the growth of our people.
"""
for index, row in filtered_df.iterrows():
    input_str = str(row['Input'])
    instruction_str = str(row['AI Instruction'])
    template_content_input = "Content input (File, URLs, Paste text or Select from Library/ Raw Responses)"
    template_topic = "- Topic"
    template_output_req = "Output requirement"
    template_output_req_1 = "Output must include"
    template_output_req_2 = "Output include"
    if template_content_input.lower() in input_str.lower():
        input_str = input_str.replace(template_content_input, f"{template_content_input}:")
    if template_topic in input_str:
        input_str = input_str.replace(template_topic, f"{template_topic}:")

    if template_output_req.lower() in instruction_str:
        instruction_str = instruction_str.replace(template_output_req, f"- {template_output_req}:")
    if template_output_req_1 in instruction_str:
        instruction_str = instruction_str.replace(template_output_req_1, f"- {template_output_req_1}:")
        print(f"instruction_str: {instruction_str}")
        break
    if template_output_req_2 in instruction_str:
        instruction_str = instruction_str.replace(template_output_req_2, f"- {template_output_req_2}:")

    test_case = f"{row['Task']} {row['Output']} that {row['Description']}\nInput: \n{input_str}\nInstruction:\n{instruction_str}"
    output_df['Task Name'] = filtered_df['Output']
    output_df.loc[index, 'Test Case'] = test_case

# --- Save to CSV ---
test_case_file = "app/workflows/employer_branding_company/unit_test/testcase_unit_gen.csv"
output_df.to_csv(test_case_file, index=False)
print(f"✅ {test_case_file} has been created.")
