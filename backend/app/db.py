from functools import lru_cache

import redis
from pymongo import MongoClient

from .config import settings


@lru_cache(maxsize=1)
def get_mongo_client() -> MongoClient:
    return MongoClient(settings.mongo_uri)


def get_urls_collection():
    client = get_mongo_client()
    return client[settings.mongo_db]["urls"]


@lru_cache(maxsize=1)
def get_redis_client() -> redis.Redis:
    return redis.Redis.from_url(settings.redis_url, decode_responses=True)
