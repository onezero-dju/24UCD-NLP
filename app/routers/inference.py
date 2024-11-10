from fastapi import APIRouter
from app.nlp.model_handler import BasicHandler
# from app.config import MODEL_PATH

router = APIRouter()

# model_handler = ModelHandler(MODEL_PATH)
model_handler = BasicHandler()

@router.post("/lm_greet")
async def greet():
    lm_greeting = model_handler.lm_greet()
    return {"lm_greet": lm_greeting}

@router.post("/answer")
async def answer(question: dict):
    answering = model_handler.custom_question_answer(question)
    return {"응답": answering}

@router.post("/summarize")
async def summarize(transcript):
    summary = model_handler