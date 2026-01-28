from fastapi import FastAPI
from pydantic import BaseModel
from scripts.rag_sire import answer_question
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ✅ CORS FIX (THIS IS THE KEY)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow frontend
    allow_credentials=True,
    allow_methods=["*"],   # allow POST, OPTIONS, etc.
    allow_headers=["*"],
)

class QuestionRequest(BaseModel):
    question: str

@app.post("/ask")
def ask_question(req: QuestionRequest):
    return answer_question(req.question)
