from app.routes import predict
from fastapi import FastAPI
from typing import Union

app = FastAPI()
app.include_router(predict.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}