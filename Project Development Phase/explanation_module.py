from gemini_utils import generate_with_fallback


def explain_topic(client, topic: str, model_name: str) -> str:
    prompt = f"""
You are EduGenie, a friendly educational tutor.

Explain this topic to a beginner:
{topic}

Use exactly these sections:
1. Simple definition
2. How it works
3. Easy example
4. Important points
5. Quick recap

Use simple English. Avoid unnecessary jargon.
"""
    response = generate_with_fallback(client, prompt, model_name)
    return response.text or "No explanation was generated."
