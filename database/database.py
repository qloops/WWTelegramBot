import logging
from typing import Optional, List, Any, Dict, Tuple
from bson import ObjectId

from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from pymongo.cursor import Cursor 
from pymongo.errors import ConnectionFailure
from pymongo.results import UpdateResult
from dataclasses import asdict

from .repositories import (
    UserRepository, 
    UserSettingsRepository, 
    UserProfileRepository,
    MediaCacheRepository
)

logger = logging.getLogger(__name__)


class MongoDBInterface:
    _client: Optional[MongoClient]
    _db: Optional[Database]
    
    # Repositories
    users: UserRepository
    users_settings: UserSettingsRepository
    users_profiles: UserProfileRepository
    media_cache: MediaCacheRepository

    def __init__(self, db_name: str, host: str = "localhost", port: int = 27017) -> None:
        self._client = None
        self._db = None

        try:
            self._client = MongoClient(host, port, serverSelectionTimeoutMS=5000)
            self._db = self._client[db_name]
            self._db.command("ping")
            
            self._init_repositories()
            
        except ConnectionFailure as e:
            raise ConnectionFailure(f"Could not connect to MongoDB at {host}:{port}: {e}")
        except Exception as e:
            if self._client:
                self._client.close()
            raise Exception(f"An unexpected error occurred during MongoDB connection: {e}")
    
    def _init_repositories(self):
        self.users = UserRepository(self)
        self.users_settings = UserSettingsRepository(self)
        self.users_profiles = UserProfileRepository(self)
        self.media_cache = MediaCacheRepository(self)

    def close(self):
        if self._client:
            self._client.close()
    
    def _get_collection(self, collection_name: str) -> Collection:
        return self._db[collection_name]

    def _insert_one(self, collection_name: str, record: Any) -> ObjectId:
        collection = self._get_collection(collection_name)
        document_to_insert = asdict(record)
        result = collection.insert_one(document_to_insert)
        return result.inserted_id

    def _insert_many(self, collection_name: str, records: List[Any]) -> List[ObjectId]:
        collection = self._get_collection(collection_name)
        documents_to_insert = [asdict(r) for r in records]
        result = collection.insert_many(documents_to_insert)
        return result.inserted_ids

    def _update_one(
        self, 
        collection_name: str, 
        query: Dict[str, Any], 
        update_operations: Dict[str, Any]
    ) -> UpdateResult:
        collection = self._get_collection(collection_name)
        return collection.update_one(query, update_operations)

    def _update_many(
        self,
        collection_name: str,
        query: Dict[str, Any],
        update_operations: Dict[str, Any]
    ) -> UpdateResult:
        collection = self._get_collection(collection_name)
        return collection.update_many(query, update_operations)

    def _find_one(
        self,
        collection_name: str,
        query: Dict[str, Any],
        projection: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        collection = self._get_collection(collection_name)
        return collection.find_one(filter=query, projection=projection)

    def _find_many(
        self,
        collection_name: str,
        query: Dict[str, Any],
        projection: Optional[Dict[str, Any]] = None,
        limit: int = 0, 
        skip: int = 0,
        sort: Optional[List[Tuple[str, int]]] = None
    ) -> List[Dict[str, Any]]:
        collection = self._get_collection(collection_name)
        cursor: Cursor = collection.find(filter=query, projection=projection)
        
        if sort:
            cursor = cursor.sort(sort)
        if skip > 0:
            cursor = cursor.skip(skip)
        if limit > 0:
            cursor = cursor.limit(limit)

        return list(cursor)


db_interface = MongoDBInterface(db_name="WW-Telegram-Bot")