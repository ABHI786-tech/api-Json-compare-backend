# Backend — JSON Compare Service

This folder contains the FastAPI backend for the JSON Compare tool. It provides a simple API to store and retrieve JSON comparison records and persists them using SQLAlchemy.

**Quick summary**
- **Framework:** FastAPI
- **ORM:** SQLAlchemy
- **App entry:** `main.py`
- **DB config:** `config/database.py` (reads `DATABASE_URL` from `Backend/.env` or `POSTGRES_SQL_DATABASE`)

**Project structure (key files)**
- `main.py` — application entry, DB initialization, router registration
- `config/database.py` — SQLAlchemy engine, session and `get_db()` dependency
- `models/json_comparison.py` — `JSONComparison` SQLAlchemy model
- `routers/json_comparison.py` — API routes for creating & fetching comparisons
- `schemas/json_comparison.py` — Pydantic request/response models
- `requirements.txt` — Python dependencies

**Architecture (Mermaid)**

```mermaid
  flowchart LR
    Client[Client] -->|HTTP Request| API[main.py]

    API --> Router[routers/json_comparison.py]

    Router --> Schema[schemas/json_comparison.py]
    Router --> Model[models/json_comparison.py]

    API -->|Uses DB Session| Config[config/database.py]
    Config --> DB[(Database)]
```

Notes:
- The Create endpoint path in the code is `/josn` (likely a typo) — the backend currently registers:
  - `POST /josn` — create a new JSON comparison (response model: `JSONComparisonResponse`)
  - `GET /json` — retrieve all comparisons
  - `GET /json/{comparison_id}` — retrieve a single comparison by `id`

Environment and setup
---------------------

Prerequisites: Python 3.10+ and a running database (Postgres or any DB compatible with `DATABASE_URL`).

1. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

2. Provide database URL:
- Create or update `Backend/.env` (or set `POSTGRES_SQL_DATABASE`) with `DATABASE_URL` pointing to your database, for example:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/json_compare_db
```

3. Run the app (development):

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

API examples
------------

- Create a comparison (note the path is `/josn` in code):

```bash
curl -X POST "http://localhost:8000/josn" \
  -H "Content-Type: application/json" \
  -d '{"json1": {"a":1}, "json2": {"a":2}, "comparison_result": {"diff":"a changed"}}'
```

- Get all comparisons:

```bash
curl http://localhost:8000/json
```

- Get one comparison by id (example id = 1):

```bash
curl http://localhost:8000/json/1
```

Models
------

`JSONComparison` (in `models/json_comparison.py`) fields:
- `id: int` (PK)
- `json1: JSON` (original JSON)
- `json2: JSON` (other JSON)
- `comparison_result: JSON` (diff/result, optional)
- `created_at: datetime`

Troubleshooting
---------------
- If the app fails on startup with a DB error, verify `DATABASE_URL` is set and reachable.
- If you expect `POST /json` but the create endpoint doesn't work, the create route path in `routers/json_comparison.py` is `/josn` — consider renaming to `/json` if desired.

Contributing / Next steps
-------------------------
- Fix route typo `/josn` → `/json` (in `routers/json_comparison.py`) if you want consistent naming.
- Add tests for endpoints and DB integration.
- Add OpenAPI examples or request/response examples in the router docstrings.

If you want, I can also open a small PR that renames the create route to `/json` and updates README examples accordingly.
