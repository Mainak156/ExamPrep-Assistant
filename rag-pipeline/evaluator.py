from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Groq Llama 3 LLM
llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile"
)

def evaluate_answer(question, correct_context, user_answer):
    prompt = f"""
You are an exam evaluator who checks the correctness of student answers based on reference content and has more than 15 years of experience.

Question: {question}
Reference Book Content: {correct_context}
Student's Answer: {user_answer}

Check if the answer is correct based on the reference content.
**If not, check if the answer is correct based on common knowledge.**
Provide marks out of 10 and give a brief 1-sentence feedback.

Return strictly in this JSON format:
{{"marks": <number>, "feedback": "<text>"}}
"""
    response = llm.invoke(prompt)
    return response.content
