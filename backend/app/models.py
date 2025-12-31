from datetime import datetime
from typing import Optional

from pydantic import BaseModel, HttpUrl


class UrlCreate(BaseModel):
    long_url: HttpUrl


class UrlResponse(BaseModel):
    short_code: str
    short_url: str
    long_url: HttpUrl
    active: bool
    created_at: datetime


class UrlRecord(BaseModel):
    short_code: str
    long_url: str
    active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
