# EduGenie — Google Gemini Powered Learning Assistant

EduGenie is a lightweight AI-powered educational assistant built with FastAPI, HTML/CSS/JavaScript, and the Google Gemini API.

## Features

- Smart Q&A
- Simple concept explanations
- Educational text summarization
- 3-question MCQ quiz generation
- Immediate quiz feedback and score
- Beginner-to-advanced learning paths
- Responsive presentation-ready web interface
- FastAPI REST endpoints
- Health check endpoint for deployment

## Architecture

Browser
  -> HTML/CSS/JavaScript
  -> FastAPI
  -> Module
  -> Gemini API
  -> Response
  -> Browser

## Project structure

EduGenie/
├── main.py
├── qna.py
├── explanation_module.py
├── quiz_module.py
├── summary_module.py
├── learning_path.py
├── requirements.txt
├── .env.example
├── .gitignore
├── render.yaml
├── README.md
├── templates/
│   └── index.html
└── static/
    ├── style.css
    └── app.js

## Local Windows setup

1. Install Python 3.10+.
2. Open Command Prompt in this folder.
3. Create a virtual environment:

   python -m venv venv

4. Activate it:

   venv\Scripts\activate

5. Install dependencies:

   pip install -r requirements.txt

6. Copy `.env.example` to `.env`.
7. Put your Gemini API key in `.env`.
8. Start the application:

   uvicorn main:app --reload

9. Open:

   http://127.0.0.1:8000

FastAPI documentation:

   http://127.0.0.1:8000/docs

Health check:

   http://127.0.0.1:8000/health

## Gemini API key

Create/manage your Gemini API key in Google AI Studio.

Never put the real API key into source code or GitHub.

## Deployment on Render

This project includes `render.yaml`.

Option A — Blueprint:
1. Push this project to GitHub.
2. In Render, create a Blueprint and select the repository.
3. Set `GEMINI_API_KEY` as a secret environment variable.
4. Deploy.

Option B — Web Service:
- Runtime: Python
- Build command: pip install -r requirements.txt
- Start command: uvicorn main:app --host 0.0.0.0 --port $PORT
- Environment variable:
  GEMINI_API_KEY = your real Gemini API key
- Optional:
  GEMINI_MODEL = gemini-3.8-flash

After deployment, open the generated Render URL.

## Important

The API key is a secret. Do not commit `.env`.

## Suggested demo sequence

1. Open EduGenie.
2. Ask: "Which is the largest ocean?"
3. Choose Explain and enter "Pythagoras theorem".
4. Choose Summarize and paste an educational paragraph.
5. Choose Quiz and enter "Photosynthesis".
6. Answer the generated questions and show the score.
7. Choose Learning Path and enter "SQL".
8. Open `/docs` to demonstrate the FastAPI endpoints.

## College project modules

Q&A:
POST /qa

Explanation:
POST /explain

Quiz:
POST /quiz

Summary:
POST /summarize

Learning recommendations:
POST /learn/recommendations

Health:
GET /health
