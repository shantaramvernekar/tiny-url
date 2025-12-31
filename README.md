## Tiny URL

This repository contains a FastAPI backend and a React UI for a URL shortening
service. The service supports generating short URLs, redirecting short URLs to
long URLs, and activating/deleting existing short URLs.

### Backend

```
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Environment variables:

- `MONGO_URI` (default: `mongodb://localhost:27017`)
- `MONGO_DB` (default: `tiny_url`)
- `REDIS_URL` (default: `redis://localhost:6379/0`)
- `BASE_URL` (default: `http://localhost:8000`)

### Frontend

```
cd frontend
npm install
npm run dev
```

Set `VITE_API_BASE` if the API runs on a different host.
