from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

app = FastAPI(
    title="Fintech RAG Research Assistant",
    description="AI-powered research assistant for SEC 10-K filings using RAG and GPT",
    version="0.1.0",
)


class QuestionRequest(BaseModel):
    question: str


@app.get("/health")
def health_check():
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat() + "Z"}


@app.get("/filings")
def list_filings():
    from pathlib import Path
    raw_dir = Path(__file__).resolve().parents[1] / "data" / "raw"
    files = [f.name for f in raw_dir.glob("*.pdf")]
    return {
        "filings": files,
        "count": len(files),
    }


@app.post("/ask")
def ask_question(request: QuestionRequest):
    from .retriever import ask
    response = ask(request.question)
    return {
        "question": response["question"],
        "answer": response["answer"],
        "sources": response["sources"],
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }