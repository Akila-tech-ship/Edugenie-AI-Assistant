# EduGenie Project Notes

## Project title

EduGenie: Google Gemini Powered Learning Assistant

## Objective

Build an educational assistant that helps learners ask questions, understand difficult concepts, summarize study material, test their knowledge, and follow structured learning paths.

## Technology stack

Frontend:
- HTML5
- CSS3
- JavaScript

Backend:
- Python
- FastAPI
- Uvicorn
- Jinja2

AI:
- Google Gemini API
- Gemini 3.8 Flash

Configuration:
- python-dotenv
- Pydantic

## Module mapping

1. qna.py
   Handles general educational question answering.

2. explanation_module.py
   Converts difficult topics into beginner-friendly explanations.

3. summary_module.py
   Creates concise revision-oriented summaries.

4. quiz_module.py
   Generates exactly three MCQs with four options each using structured output.

5. learning_path.py
   Generates a beginner-to-advanced learning roadmap.

6. main.py
   Provides the FastAPI application and REST endpoints.

7. templates/index.html
   Provides the main web interface.

8. static/style.css
   Provides responsive visual design.

9. static/app.js
   Connects the frontend to the FastAPI backend and handles quiz interactions.

## API endpoints

GET /
POST /qa
POST /explain
POST /summarize
POST /quiz
POST /learn/recommendations
GET /health

## Demo inputs

Q&A:
Which is the largest ocean?

Explain:
Pythagoras theorem

Summary:
Paste a paragraph about photosynthesis.

Quiz:
Photosynthesis

Learning Path:
SQL

## Viva explanation

When a user selects a feature, JavaScript sends a POST request to the matching FastAPI endpoint. FastAPI validates the request using Pydantic. The endpoint calls the corresponding Python module. The module creates an educational prompt and sends it to Gemini. The Gemini response is returned as JSON to the browser. The frontend then renders the result.

## Future enhancements

- User authentication
- Learning history
- Progress dashboard
- PDF/image input
- Voice interaction
- Multilingual learning
- Persistent database
- Teacher/parent dashboard
- LMS integration
- Adaptive learning based on quiz performance
