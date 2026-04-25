# AGENTS.md

Flask API for URL shortening.

## Run
```bash
python app.py
```
Or with the venv: `source .venv/bin/activate && python app.py`

Server runs on port **9284** (not 5000).

## Endpoints
- `POST /encurtar` - Body: `{"url": "https://..."}`
- `POST /encurtar` - With custom code: `{"url": "https://...", "code": "custom"}` (min 3 chars)
- `GET /stats/<code>` - Returns `{"url_original": "...", "clicks": N}`
- `GET /<code>` - Redirects to original URL

## Dependencies
- flask
- flask-cors

## Tests
```bash
pytest -v
```

## Architecture
- `source/models/main_model.py` - Database path: `BANCO_PATH` (used by all models)
- `source/models/encurtar_model.py` - Uses `main_model.BANCO_PATH`
- `source/models/redirect_model.py` - Uses its own `BANCO_PATH`

When testing, monkeypatch all model `BANCO_PATH` constants to use a test database.