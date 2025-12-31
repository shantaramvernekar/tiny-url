from datetime import datetime

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from .config import settings
from .db import get_redis_client, get_urls_collection
from .models import UrlCreate, UrlResponse, UrlRecord
from .repository import UrlRepository
from .utils import generate_short_code

app = FastAPI(title="Tiny URL Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_repository() -> UrlRepository:
    return UrlRepository(get_urls_collection())


def build_response(record: UrlRecord) -> UrlResponse:
    return UrlResponse(
        short_code=record.short_code,
        short_url=f"{settings.base_url}/{record.short_code}",
        long_url=record.long_url,
        active=record.active,
        created_at=record.created_at,
    )


@app.post("/api/urls", response_model=UrlResponse, status_code=status.HTTP_201_CREATED)
def create_short_url(payload: UrlCreate):
    repository = get_repository()
    short_code = generate_short_code()
    while repository.get_by_code(short_code):
        short_code = generate_short_code()
    record = UrlRecord(
        short_code=short_code,
        long_url=str(payload.long_url),
        active=True,
        created_at=datetime.utcnow(),
    )
    repository.create(record)
    redis_client = get_redis_client()
    redis_client.set(short_code, record.long_url)
    return build_response(record)


@app.get("/api/urls/{short_code}", response_model=UrlResponse)
def get_short_url(short_code: str):
    repository = get_repository()
    record = repository.get_by_code(short_code)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="URL not found")
    return build_response(record)


@app.patch("/api/urls/{short_code}/activate", response_model=UrlResponse)
def activate_short_url(short_code: str):
    repository = get_repository()
    record = repository.update_active(short_code, True)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="URL not found")
    redis_client = get_redis_client()
    redis_client.set(short_code, record.long_url)
    return build_response(record)


@app.patch("/api/urls/{short_code}/deactivate", response_model=UrlResponse)
def deactivate_short_url(short_code: str):
    repository = get_repository()
    record = repository.update_active(short_code, False)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="URL not found")
    redis_client = get_redis_client()
    redis_client.delete(short_code)
    return build_response(record)


@app.delete("/api/urls/{short_code}", status_code=status.HTTP_204_NO_CONTENT)
def delete_short_url(short_code: str):
    repository = get_repository()
    deleted = repository.delete(short_code)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="URL not found")
    redis_client = get_redis_client()
    redis_client.delete(short_code)
    return None


@app.get("/{short_code}")
def redirect_short_url(short_code: str):
    redis_client = get_redis_client()
    cached = redis_client.get(short_code)
    if cached:
        return RedirectResponse(cached, status_code=status.HTTP_307_TEMPORARY_REDIRECT)

    repository = get_repository()
    record = repository.get_by_code(short_code)
    if not record or not record.active:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="URL not found")
    redis_client.set(short_code, record.long_url)
    return RedirectResponse(record.long_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT)
