from gemini_utils import generate_with_fallback


def summarize_text(client, text: str, model_name: str) -> str:
    prompt = f"""
You are EduGenie, an educational summarization assistant.

Summarize the following educational content:

{text}

Requirements:
- Preserve the important facts and original meaning.
- Remove repetition and unnecessary detail.
- Use simple language.
- Use bullet points where useful.
- Finish with a one-sentence revision takeaway.
"""
    response = generate_with_fallback(client, prompt, model_name)
    return response.text or "No summary was generated."
