from fastapi import APIRouter
from api_custom.nlp_link.model_handlers._basic_handler import BasicHandler

router = APIRouter()

model_handler = BasicHandler()

@router.post("/lm_greet")
async def greet():
    lm_greeting = model_handler.lm_greet()
    return {"lm_greet": lm_greeting}

@router.post("/answer")
async def answer(question: dict):
    answering = model_handler.custom_question_answer(question)
    return {"응답": answering}
