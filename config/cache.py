import json
from typing import Any

from config.redis import CACHE_TTL_SECONDS, get_redis

ALL_COMPARISONS_KEY = "comparisons:all"


def comparison_key(comparison_id: int) -> str:
    return f"comparisons:{comparison_id}"


def cache_get(key: str) -> Any | None:
    client = get_redis()
    if client is None:
        return None

    cached = client.get(key)
    if cached is None:
        return None

    return json.loads(cached)


def cache_set(key: str, value: Any, ttl: int = CACHE_TTL_SECONDS) -> None:
    client = get_redis()
    if client is None:
        return

    client.setex(key, ttl, json.dumps(value, default=str))


def cache_delete(*keys: str) -> None:
    client = get_redis()
    if client is None or not keys:
        return

    client.delete(*keys)


def invalidate_list_cache() -> None:
    cache_delete(ALL_COMPARISONS_KEY)


def invalidate_item_cache(comparison_id: int) -> None:
    cache_delete(comparison_key(comparison_id))
