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

def user_prompt(cv_text):
    return f"""
        You are a resume expert. Read the resume below and do the following:

        Resume:
        {cv_text}

        Tasks:

        1. **Professional Summary**:  
        Write a short paragraph that explains the person's work experience, main skills, and strengths. Use your own words. Do not copy from the resume. Write it in a natural and professional way.

        2. **JSON Output**:  
        Create a JSON in this format:
        {{
            "key_skills": {{
                "professional_skills": ["List of job or technical skills"],
                "soft_skills": ["List of personal or people skills"]
            }},

            "experience_summary": {{
                "job_title": "Job Title",
                "company": "Leave blank if company name is not mentioned and answer Not mentioned",
                "duration": "Time Period",
            }},

            "job_description": {{
                "description": "Summarize the main responsibilities and duties in this role, using your own words within 50 to 10"
            }}
            ... 
        }}

        Guidlines:
        - Use the resume text provided above.
        - Do not include the resume text in your response.
        - If soft skills are not mentioned, add them using the uploaded reference file.

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

    summary_match = re.search(r"\*\*Professional Summary\*\*:\s*(.*?)\n\s*\n", result, re.DOTALL)
    professional_summary = summary_match.group(1).strip()
    print("**Professional Summary**:\n")
    print(professional_summary)


    extracted_json = extract_json_from_text(result)
    if extracted_json:
        print("\n**JSON Output**:\n")
        print(json.dumps(extracted_json, indent=4))
    else:
        print("No valid JSON found.")

# Example usage
if __name__ == '__main__':
    analyze_cv_from_pdf("CV2.pdf")