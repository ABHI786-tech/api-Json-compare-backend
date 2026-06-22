import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import OperationalError

from config import Base, engine
from routers import json_comparison_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5173",
        "http://localhost:5173",
        "http://127.0.0.1:4321",
        "http://localhost:4321",
        "http://127.0.0.1:3000",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def init_db(retries: int = 10, delay: float = 2.0) -> None:
    for attempt in range(1, retries + 1):
        try:
            Base.metadata.create_all(bind=engine)
            return
        except OperationalError:
            if attempt == retries:
                raise
            time.sleep(delay)


@app.on_event("startup")
def on_startup() -> None:
    init_db()


app.include_router(json_comparison_router)


@app.get("/")
def home():
    return "hello abhi"