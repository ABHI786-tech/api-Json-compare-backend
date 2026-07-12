import os
from pathlib import Path

import redis
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
CACHE_TTL_SECONDS = int(os.getenv("CACHE_TTL_SECONDS", "300"))

_redis_client: redis.Redis | None = None


def connect_redis() -> bool:
    global _redis_client
    try:
        client = redis.from_url(REDIS_URL, decode_responses=True)
        client.ping()
        _redis_client = client
        return True
    except redis.RedisError:
        _redis_client = None
        return False


def disconnect_redis() -> None:
    global _redis_client
    if _redis_client is not None:
        _redis_client.close()
        _redis_client = None


def get_redis() -> redis.Redis | None:
    return _redis_client


def is_redis_available() -> bool:
    if _redis_client is None:
        return False
    try:
        _redis_client.ping()
        return True
    except redis.RedisError:
        return False
