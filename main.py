import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import OperationalError

from config import Base, engine
from config.cors import get_cors_origins
from config.redis import connect_redis, disconnect_redis, is_redis_available
from routers import json_comparison_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_cors_origins(),
    # allow_origins=[*]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
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
    connect_redis()


@app.on_event("shutdown")
def on_shutdown() -> None:
    disconnect_redis()


app.include_router(json_comparison_router)


@app.get("/")
def home():
    return {
        "message": "hello abhi",
        "redis": "connected" if is_redis_available() else "unavailable",
    }
