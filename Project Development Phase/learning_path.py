from gemini_utils import generate_with_fallback


def get_learning_recommendations(client, topic: str, model_name: str) -> str:
    prompt = f"""
You are EduGenie, a personalized learning advisor.

Create a practical learning path for:
{topic}

Organize it into:
1. Prerequisites
2. Beginner level
3. Intermediate level
4. Advanced level
5. Practice projects
6. Suggested weekly schedule
7. Final project

For each level, include:
- Topics to learn
- What the learner should be able to do
- Approximate learning time

Recommend resource TYPES such as official documentation,
courses, videos, articles, books, and practice platforms.
Do not invent specific URLs.
Use simple, clear language.
"""
    response = generate_with_fallback(client, prompt, model_name)
    return response.text or "No learning path was generated."
