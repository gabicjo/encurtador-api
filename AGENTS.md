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

## Dependencies
- flask
- flask-cors