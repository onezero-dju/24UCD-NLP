from api_custom.routers import _test_lm_comm as test, transcript_nlp
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Union

app = FastAPI()
app.include_router(test.router)
app.include_router(transcript_nlp.router)

# Define allowed origins (React app's URL)
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,             # Allowed origins
    allow_credentials=True,
    allow_methods=["*"],               # Allow all HTTP methods
    allow_headers=["*"],               # Allow all headers
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
