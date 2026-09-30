from gemini_utils import generate_with_fallback


def answer_question(client, question: str, model_name: str) -> str:
    prompt = f"""
You are EduGenie, an educational AI assistant.

Answer the student's question accurately and clearly.

Student question:
{question}

Instructions:
- Give the direct answer first.
- Use simple, student-friendly language.
- Explain difficult terms when necessary.
- Use short sections or bullets when helpful.
- Do not unnecessarily make the response long.
"""
    response = generate_with_fallback(client, prompt, model_name)
    return response.text or "No answer was generated."
