from fastapi import APIRouter
from app.ml_models.model_handler import ModelHandler
# from app.config import MODEL_PATH

router = APIRouter()

# model_handler = ModelHandler(MODEL_PATH)
model_handler = ModelHandler()

@router.post("/lm_greet")
async def predict(data: dict):
    lm_greeting = model_handler.lm_greet(data)
    return {"lm_greet": lm_greeting}

@router.post("/answer")
async def answer(question: dict):
    answering = model_handler.answer(question)
    return {"응답": answering}