import os
import json
from google import genai

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def resume_analysis_prompt(resume_text, user_goal, experience):
    return f"""
    You are a senior software engineer and hiring manager.

    Evaluate the resume based on the user goal and their experience level.

    User goal: "{user_goal}"
    Target Role Seniority: "Looking for a role requiring ~{experience} years of experience"
    Resume text: "{resume_text}"

    # STRICT RULES:
    - Extract only relevent skills for this goal
    - Remove irrelevent tools like: [excel for backend dev, etc]
    - Identify real gaps
    - Generate roadmap only for missing skills or fields
    - Make output DIFFERENT based on goal.

    Return response in ONLY JSON format.
    {{
        "skills": ["skill1", "skill2"],
        "missing_skills": ["skill3", "skill4"],
        "roadmap": [
            {"skill": "Skill Name", "description": "Detailed learning path"}
        ],
        "interview_questions": [
            {"question": "The Question", "answer": "The ideal answer"}
        ]
    }}
    """

def analyze_resume(resume_text, user_goal, experience):
    prompt = resume_analysis_prompt(resume_text, user_goal, experience)

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash-lite',
            contents=prompt,
            config={
                'temperature': 0.3,
            }
        )

        result_text = response.text.strip()

        # What this logic doing step by step: 
        # 1. Import the re module (regular expressions)
        # 2. Use re.search() to find the first occurrence of the pattern r'\{.*\}'
        # 3. The pattern r'\{.*\}' matches: 
        #    - \{ : A literal opening curly brace
        #    - .* : Any character (.), zero or more times (*)
        #    - \} : A literal closing curly brace
        #    - The re.DOTALL flag makes . match newline characters as well
        # 4. The search looks for the first { ... } block in the result_text
        # 5. If a match is found, it extracts the matched substring and assigns it to result_text
        
        import re
        match = re.search(r'\{.*\}', result_text, re.DOTALL)
        if match:
            result_text = match.group(0)
            
        return json.loads(result_text)
    
    except Exception as e:
        return {"error": str(e)}

