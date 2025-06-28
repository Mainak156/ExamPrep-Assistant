import json
import re
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Groq Llama 3 LLM
llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile"
)

def generate_questions(context, topic, question_type="MCQ", num_questions=10, max_retries=5):
    if not context.strip():
        print("❌ No context received for question generation.")
        return []

    prompt_template = f"""
You are a reliable exam question paper generator akin to a professor of a well-esteemed, reputed university who carefully checks the inner knowledge of students.

Based on the study content below, generate exactly {num_questions} {question_type} questions.

**IMPORTANT: Only generate questions strictly related to the topic: "{topic}". Do not include other concepts unless they are directly connected to "{topic}".**

Study Content:
\"\"\"{context}\"\"\"

Instructions:
- Generate questions only from the above context.
- Return **only a valid JSON array** with no explanation or pre-text.
- Do not prefix the JSON with any commentary.
- Example for MCQ:
[
  {{
    "question": "What is a recurrence relation?",
    "options": ["A) Option 1", "B) Option 2", "C) Option 3", "D) Option 4"]
  }}
]

Now generate and return the JSON array.
"""


    attempt = 0
    while attempt < max_retries:

        response = llm.invoke(prompt_template)
        content = response.content.strip()

        # Extract JSON array using regex
        json_match = re.search(r'\[\s*{.*?}\s*\]', content, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
            try:
                questions = json.loads(json_str)
                if isinstance(questions, list) and len(questions) > 0:
                    print(f"✅ {len(questions)} Question(s) Generated!")
                    return questions
                else:
                    print("⚠️ Parsed JSON but empty or invalid format.")
            except (json.JSONDecodeError, ValueError) as e:
                print(f"⚠️ JSON parsing failed on attempt {attempt+1}: {e}")
        else:
            print(f"⚠️ No valid JSON array found in LLM response on attempt {attempt+1}")

        attempt += 1

    print("❌ Failed to generate valid JSON after retries.")
    return []
