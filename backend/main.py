from fastapi import FastAPI
from pydantic import BaseModel
from scripts.rag_sire import answer_question

app = FastAPI(title="IndiGuide-QA API")

class QuestionRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    answer: str
    sources: list[str]

@app.post("/ask", response_model=AnswerResponse)
def ask_question(req: QuestionRequest):
    result = answer_question(req.question)
    return result
