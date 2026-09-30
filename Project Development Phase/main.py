import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from google import genai

from qna import answer_question
from explanation_module import explain_topic
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations
from gemini_utils import get_model_candidates

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("GEMINI_MODEL") or "gemini-3.8-flash"
client = genai.Client(api_key=API_KEY) if API_KEY else None

app = FastAPI(
    title="EduGenie",
    description="Google Gemini Powered Learning Assistant",
    version="1.0.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["null"],
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1):(5500|5501|4173|3000)",
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


class TextRequest(BaseModel):
    text: str


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.get("/health")
async def health():
    return {
        "status": "healthy" if client else "configuration_required",
        "service": "EduGenie",
        "gemini_configured": client is not None,
    }


@app.post("/qa")
async def qa(request: TextRequest):
    validate_text(request.text, "question")
    require_gemini_client()
    try:
        return {"success": True, "result": answer_question(client, request.text, MODEL_NAME)}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=safe_error(exc))


@app.post("/explain")
async def explain(request: TextRequest):
    validate_text(request.text, "topic")
    require_gemini_client()
    try:
        return {"success": True, "result": explain_topic(client, request.text, MODEL_NAME)}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=safe_error(exc))


@app.post("/summarize")
async def summarize(request: TextRequest):
    validate_text(request.text, "text")
    require_gemini_client()
    try:
        return {"success": True, "result": summarize_text(client, request.text, MODEL_NAME)}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=safe_error(exc))


@app.post("/quiz")
async def quiz(request: TextRequest):
    validate_text(request.text, "topic")
    require_gemini_client()
    try:
        return {"success": True, "result": generate_quiz(client, request.text, MODEL_NAME)}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=safe_error(exc))


@app.post("/learn/recommendations")
async def learning_recommendations(request: TextRequest):
    validate_text(request.text, "topic")
    require_gemini_client()
    try:
        return {
            "success": True,
            "result": get_learning_recommendations(
                client, request.text, MODEL_NAME
            ),
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=safe_error(exc))


def validate_text(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise HTTPException(
            status_code=400,
            detail=f"Please enter a {field_name}.",
        )


def require_gemini_client():
    if client is None:
        raise HTTPException(
            status_code=503,
            detail="Gemini is not configured. Set GEMINI_API_KEY in .env and restart EduGenie.",
        )
    return client


def safe_error(exc: Exception) -> str:
    # Avoid returning secrets or environment details to the browser.
    message = str(exc).strip()
    if not message:
        return "EduGenie could not complete the request."
    return message[:500]


def get_model_candidates_for_debug():
    return get_model_candidates(MODEL_NAME)
