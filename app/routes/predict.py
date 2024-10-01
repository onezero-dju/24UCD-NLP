from fastapi import APIRouter
from app.ml_models.model_handler import ModelHandler
# from app.config import MODEL_PATH

router = APIRouter()

# model_handler = ModelHandler(MODEL_PATH)
model_handler = ModelHandler()

@router.post("/predict")
async def predict(data: dict):
    prediction = model_handler.predict(data)
    return {"prediction": prediction}

@router.post("/answer")
async def answer(question: dict):
    answering = model_handler.answer(question)
    return {"응답": answering}