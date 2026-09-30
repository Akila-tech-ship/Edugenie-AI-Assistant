from typing import List

from pydantic import BaseModel, Field

from gemini_utils import generate_with_fallback


class QuizQuestion(BaseModel):
    question: str
    options: List[str] = Field(min_length=4, max_length=4)
    correct_answer: str


class QuizResponse(BaseModel):
    questions: List[QuizQuestion] = Field(min_length=3, max_length=3)


def generate_quiz(client, topic: str, model_name: str) -> dict:
    prompt = f"""
Create a student-friendly multiple-choice quiz about:

{topic}

Requirements:
- Exactly 3 questions.
- Exactly 4 options per question.
- Exactly one correct answer per question.
- Plausible distractors.
- Questions should test understanding.
- Keep the language clear and concise.
"""

    response = generate_with_fallback(
        client,
        prompt,
        model_name,
        response_schema=QuizResponse,
    )

    quiz = QuizResponse.model_validate_json(response.text)
    return quiz.model_dump()
