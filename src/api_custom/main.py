from api_custom.routers import _test_lm_comm as test, transcript_nlp
from fastapi import FastAPI
from typing import Union

app = FastAPI()
app.include_router(test.router)
# app.include_router(transcript_nlp.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}