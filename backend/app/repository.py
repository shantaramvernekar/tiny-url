from datetime import datetime
from typing import Optional

from pymongo import ReturnDocument
from pymongo.collection import Collection

from .models import UrlRecord


class UrlRepository:
    def __init__(self, collection: Collection):
        self.collection = collection

    def create(self, record: UrlRecord) -> UrlRecord:
        payload = record.dict()
        self.collection.insert_one(payload)
        return record

    def get_by_code(self, short_code: str) -> Optional[UrlRecord]:
        data = self.collection.find_one({"short_code": short_code})
        if not data:
            return None
        data.pop("_id", None)
        return UrlRecord(**data)

    def update_active(self, short_code: str, active: bool) -> Optional[UrlRecord]:
        updated_at = datetime.utcnow()
        result = self.collection.find_one_and_update(
            {"short_code": short_code},
            {"$set": {"active": active, "updated_at": updated_at}},
            return_document=ReturnDocument.AFTER,
        )
        if not result:
            return None
        result.pop("_id", None)
        return UrlRecord(**result)

    def delete(self, short_code: str) -> bool:
        result = self.collection.delete_one({"short_code": short_code})
        return result.deleted_count > 0
