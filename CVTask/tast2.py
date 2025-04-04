import json
import os
import re
from dotenv import load_dotenv
import fitz
import openai

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = openai.OpenAI(api_key=api_key)

def read_pdf_text(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text


def system_prompt():
    return (
        "You are an AI assistant that analyzes resume data. "
        "You provide a short, well-written summary of the candidate in paragraph form, "
        "and return skills and experience details in clean JSON format."
    )

# def user_prompt(cv_text):
#     return f"""
#         You are a resume expert. Read the resume below and complete the following tasks:

#         Resume:
#         {cv_text}

#         **Tasks**

#         1. **Professional Summary**  
#         Write a short paragraph summarizing the candidate`s work experience, key technical strengths, and soft skills. Use a natural, professional tone.

#         2. **Job Role Recommendations**  
#         Based on the candidate`s experience and professional skills, suggest 3 to 4 suitable job titles.

#         3. **Suggested Upskilling**  
#         Analyze the current professional skills and recommend 2 to 5 new skills or technologies the candidate should consider learning.  
#         For each suggested skill, estimate how strong the job market demand is in the near future (out of 100).

#         4. **JSON Output**  
#         Return a clean and structured JSON response in this format:

#         {{
#         "key_skills": {{
#             "professional_skills": ["List of job-related or technical skills"],
#             "soft_skills": ["List of interpersonal or behavioral skills"]
#         }},

#         "experience_summary": [
#             {{
#             "job_title": "Job Title",
#             "company": "Company name (use 'Not mentioned' if missing)",
#             "duration": "Time period as listed in the resume",
#             }}, ...
#             ],
#             "job_descriptions": {{
#                 "Job Title 1": "Summarize the main responsibilities and duties for this role keeping it between 50-100 words.",
#                 "Job Title 2": "Summary for second role",
#                 ...
#             }}
#         }}

#         **Guidelines**

#         - Use only the resume data provided above.
#         - Do not quote or repeat the resume text.
#         - Infer soft skills and upskilling based on resume context or use the uploaded reference file.
#         - Job opportunity score reflects expected hiring demand and relevance over the next 3-5 years.
#     """
def user_prompt(cv_text):
    return f"""
    You are a resume expert. Read the resume below and complete the following tasks:

    Resume:
    {cv_text}

    **Tasks**

    1. **Professional Summary**  
    Write a short paragraph summarizing the candidate’s work experience, key technical strengths, and soft skills. Use a natural, professional tone.

    2. **Job Role Recommendations**  
    Based on the candidate’s experience and professional skills, suggest 3 to 4 suitable job titles.

    3. **Suggested Upskilling**  
    Analyze the current professional skills and recommend 2 to 5 new skills or technologies the candidate should consider learning.  
    For each suggested skill, estimate how strong the job market demand is in the near future (out of 100).  
    Also provide:
    - 5 recommended online learning platforms where the candidate can learn these skills.
    - 5 to 6 high-quality YouTube channels (with channel names only) that offer relevant content for these upskilling topics.

    4. **JSON Output**  
    Return a clean and structured JSON response in this format:

    {{
    "key_skills": {{
        "professional_skills": ["List of job-related or technical skills"],
        "soft_skills": ["List of interpersonal or behavioral skills"]
    }},
    "experience_summary": [
        {{
            "job_title": "Job Title",
            "company": "Company name (use 'Not mentioned' if missing)",
            "duration": "Time period as listed in the resume"
        }},
        ...
    ],
    "job_descriptions": {{
        "Job Title 1": "Summarize the main responsibilities and duties for this role keeping it between 50–100 words.",
        "Job Title 2": "Summary for second role",
        ...
    }}
    }}

    **Guidelines**

    - Use only the resume data provided above.
    - Do not quote or repeat the resume text.
    - Infer soft skills and upskilling based on resume context or use the uploaded reference file.
    - Job opportunity score reflects expected hiring demand and relevance over the next 3–5 years.
    - Learning platforms and YouTube channels must be tailored to the skills suggested.
    """


def extract_json_from_text(text):
    try:
        json_match = re.search(r'\{[\s\S]*\}', text)
        if json_match:
            json_data = json.loads(json_match.group())
            return json_data
    except json.JSONDecodeError as e:
        print("JSON parsing error:", e)
    return None

def analyze_cv_from_pdf(pdf_path):
    cv_text = read_pdf_text(pdf_path)
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt()},
            {"role": "user", "content": user_prompt(cv_text)},
        ],
        max_tokens=450
    )

    result = response.choices[0].message.content

    # summary_match = re.search(r"\*\*Professional Summary\*\*:\s*(.*?)\n\s*\n", result, re.DOTALL)
    # professional_summary = summary_match.group(1).strip()
    # print("**Professional Summary**:\n")
    # print(professional_summary)
    print(result)

    # extracted_json = extract_json_from_text(result)
    # if extracted_json:
    #     print("\n**JSON Output**:\n")
    #     print(json.dumps(extracted_json, indent=4))
    # else:
    #     print("No valid JSON found.")

# Example usage
if __name__ == '__main__':
    analyze_cv_from_pdf("CV2.pdf")
    