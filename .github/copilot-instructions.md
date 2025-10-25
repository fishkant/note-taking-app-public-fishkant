## Quick orientation — NoteTaker project

This repository is a small Flask + SQLite single-repo app with a static frontend served from `src/static/index.html`. Key artifacts:

- Backend entry: `src/main.py` (Flask app, registers blueprints `user_bp` and `note_bp` under `/api`).
- Models: `src/models/user.py`, `src/models/note.py` (SQLAlchemy `db` is defined in `user.py`).
- Frontend: `src/static/index.html` (served by Flask `app.static_folder`).
- LLM helper: `src/llm.py` (wrapping OpenAI client; provides `call_llm_model` and `translate_to_language`).
- Dev/test helpers: `testllm.py` (simple LLM smoke test).

## Big-picture architecture and data flow

- The Flask app (run with `python src/main.py`) serves a single-page frontend and exposes a JSON REST API under `/api` (notes endpoints live under `/api/notes`).
- Database: a file-based SQLite DB located at `database/app.db` (configured in `src/main.py`). SQLAlchemy models live in `src/models` and expose `to_dict()` for the API responses — preserve that shape when changing models (frontend expects `tags` as a list via `Note.to_dict`).
- LLM usage is isolated in `src/llm.py`. Environment configuration uses `dotenv` and expects `GITHUB_TOKEN` for the API key and a custom `endpoint` (see `src/llm.py` and `testllm.py`).

## Developer workflows (concrete commands)

1. Create and activate venv
```bash
python -m venv venv
source venv/bin/activate
```
2. Install dependencies
```bash
pip install -r requirements.txt
```
3. Run the app (default port 5001)
```bash
python src/main.py
# app will bind to 0.0.0.0:5001 by default (debug=True in main)
```
4. Quick LLM smoke test (requires `GITHUB_TOKEN` in env)
```bash
python testllm.py
```

Notes: `src/main.py` inserts the repo `src` parent dir on sys.path (don’t remove the `sys.path.insert` line). The app enables CORS globally.

## Project-specific conventions and gotchas

- Blueprint URL prefix: both `user_bp` and `note_bp` are registered with `url_prefix='/api'`. API endpoints therefore appear under `/api/...`.
- Model `to_dict()` shapes are relied on by the frontend: `Note.to_dict()` returns `tags` as a list (stored internally as comma-separated string) and formats `event_date`/`event_time`. If you change the JSON shape, update the frontend `src/static/index.html` JS accordingly.
- DB path is assembled in `src/main.py` as `database/app.db` relative to the repo root — tests and the running server share this file.
- The code uses `GITHUB_TOKEN` (not `OPENAI_API_KEY`) for the OpenAI client. `src/llm.py` sets `endpoint = "https://models.github.ai/inference"` and `model = "openai/gpt-4.1-mini"` — changing those values affects all LLM calls.

## LLM / translation integration guidance (how to add the feature)

When adding translation endpoints or UI, follow these patterns:

- Keep all LLM calls inside `src/llm.py` so the rest of the app stays testable and token handling is centralized.
- `src/llm.py` exposes `translate_to_language(text, target_language)` that calls `call_llm_model(...)`. Reuse it rather than instantiating an OpenAI client elsewhere.

Suggested API for adding a translation endpoint (example only — implement in `routes/note.py` alongside existing note handlers):

```
# POST /api/notes/<id>/translate
# body: { "target_language": "French" }
# flow: load note by id -> call src.llm.translate_to_language(note.content, target_language) -> return translated text
```

Data shapes to keep in mind:
- Request: JSON with `target_language` string.
- Response: `{ "note_id": <id>, "target_language": "French", "translated_text": "..." }`.

Security and env notes:
- LLM calls use the repo-wide `GITHUB_TOKEN` environment variable. Do not commit tokens or add them to code.
- `src/llm.py` calls `load_dotenv()` to pick up a `.env` file for local dev; CI or deployment may inject env vars differently.

## Files to inspect when working on translation or LLM features

- `src/llm.py` — LLM client wrapper (first stop for translation logic)
- `testllm.py` — quick manual LLM usage example
- `src/models/note.py` — note schema and `to_dict()` (important for API response shape)
- `src/main.py` — app wiring, blueprint registration, DB path, and static serving logic
- `src/static/index.html` — frontend expects certain JSON shapes; update it when changing API responses

## When in doubt

- Read `src/llm.py` before changing LLM or translation-related code — this file centralizes token, endpoint, and model config.
- Preserve `Note.to_dict()` output if possible. If you must change it, update the frontend and add a minimal test demonstrating the new shape.

If anything in this file is unclear or you want the instructions to include a concrete route implementation for the translator (and a small unit test), tell me and I will add that example and a matching test file.
