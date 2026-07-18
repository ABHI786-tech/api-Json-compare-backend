import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

DEFAULT_DEV_ORIGINS = [
    "https://comparejsononline.com/json",
    "https://api.comparejsononline.com",
    "http://127.0.0.1:5173",
    "http://localhost:5173",
    "http://127.0.0.1:4321",
    "http://localhost:4321",
    "http://127.0.0.1:3000",
    "http://localhost:3000",
]


def _parse_origins(value: str) -> list[str]:
    return [origin.strip().rstrip("/") for origin in value.split(",") if origin.strip()]


def get_cors_origins() -> list[str]:
    """Build allowed CORS origins from env vars, with local dev defaults."""
    origins: list[str] = []

    cors_origins = os.getenv("CORS_ORIGINS")
    if cors_origins:
        origins.extend(_parse_origins(cors_origins))

    frontend_url = os.getenv("FRONTEND_URL")
    if frontend_url:
        origins.append(frontend_url.strip().rstrip("/"))

    if not origins:
        return DEFAULT_DEV_ORIGINS.copy()

    for origin in DEFAULT_DEV_ORIGINS:
        if origin not in origins:
            origins.append(origin)

    return origins
