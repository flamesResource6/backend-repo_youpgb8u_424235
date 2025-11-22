from typing import Any, Dict, List, Optional
import os
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from fastapi import HTTPException

DATABASE_URL = os.getenv("DATABASE_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "appdb")

_client: Optional[AsyncIOMotorClient] = None
_db: Optional[AsyncIOMotorDatabase] = None

async def get_db() -> AsyncIOMotorDatabase:
    global _client, _db
    if _db is None:
        _client = AsyncIOMotorClient(DATABASE_URL)
        _db = _client[DATABASE_NAME]
    return _db

async def create_document(collection_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
    db = await get_db()
    now = datetime.utcnow()
    data_with_meta = {**data, "created_at": now, "updated_at": now}
    res = await db[collection_name].insert_one(data_with_meta)
    inserted = await db[collection_name].find_one({"_id": res.inserted_id})
    if not inserted:
        raise HTTPException(status_code=500, detail="Insert failed")
    inserted["_id"] = str(inserted["_id"])  # serialize ObjectId
    return inserted

async def get_documents(collection_name: str, filter_dict: Optional[Dict[str, Any]] = None, limit: int = 50) -> List[Dict[str, Any]]:
    db = await get_db()
    cursor = db[collection_name].find(filter_dict or {}).limit(limit)
    docs = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])  # serialize ObjectId
        docs.append(doc)
    return docs
