import logging
from typing import Optional, List, Any, Dict, Tuple
from bson import ObjectId
from dataclasses import asdict 

from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from pymongo.cursor import Cursor 
from pymongo.errors import ConnectionFailure
from pymongo.results import UpdateResult

from .models import FullUserProfile
from .models import DetectedUserProfile

logger = logging.getLogger(__name__)


class MongoDBInterface:
    _client: Optional[MongoClient]
    _db: Optional[Database]

    USERS_PROFILES_COLLECTION: str = "users_profiles"
    DETECTED_PROFILES_COLLECTION: str = "detected_profiles"

    def __init__(self,  db_name: str, host: str = "localhost", port: int = 27017) -> None:
        self._client = None
        self._db = None

        try:
            self._client = MongoClient(host, port, serverSelectionTimeoutMS=5000)
            
            self._db = self._client[db_name]
            self._db.command("ping")
        except ConnectionFailure as e:
            raise ConnectionFailure(f"Could not connect to MongoDB at {host}:{port}: {e}")
        except Exception as e:
            if self._client:
                self._client.close()
            raise Exception(f"An unexpected error occurred during MongoDB connection: {e}")

    def _get_collection(
        self, 
        collection_name: str
    ) -> Collection:
        return self._db[collection_name]

    def _insert_one(
        self, 
        collection_name: str, 
        record: Any
    ) -> ObjectId:
        collection = self._get_collection(collection_name)
        document_to_insert = asdict(record)
        result = collection.insert_one(document_to_insert)
        return result.inserted_id

    def _insert_many(
        self, 
        collection_name: str, 
        records: List[Any]
    ) -> List[ObjectId]:
        collection = self._get_collection(collection_name)
        documents_to_insert = [asdict(r)for r in records]
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

    def insert_profile(self, record: FullUserProfile) -> ObjectId:
        return self._insert_one(self.USERS_PROFILES_COLLECTION, record)

    def update_user_profile(
        self, 
        condition: Dict[str, Any], 
        updated_profile_data: FullUserProfile
    ) -> UpdateResult:
        data_to_set = asdict(updated_profile_data)
        update_document = {"$set": data_to_set}
        return self._update_one(self.USERS_PROFILES_COLLECTION, condition, update_document)
    
    def get_user_profile(self, condition: Dict[str, Any]) -> Optional[FullUserProfile]:
        doc = self._find_one(self.USERS_PROFILES_COLLECTION, condition)
        if doc:
            doc.pop("_id", None) 
            try:
                return FullUserProfile(**doc)
            except TypeError as e:
                logger.error(f"Error creating FullUserProfile for doc {condition}: {e}. Document: {doc}")
                return None 
        return None

    def get_user_profiles(
        self, 
        condition: Dict[str, Any],
        limit: int = 0,
        skip: int = 0,
        sort: Optional[List[Tuple[str, int]]] = None
    ) -> List[FullUserProfile]:
        docs = self._find_many(self.USERS_PROFILES_COLLECTION, condition, limit=limit, skip=skip, sort=sort)
        profiles: List[FullUserProfile] = []
        for doc in docs:
            doc.pop("_id", None)
            try:
                profiles.append(FullUserProfile(**doc))
            except TypeError as e:
                logger.error(f"Skipping doc due to TypeError: {e}. Document: {doc}")
                continue 
        return profiles

    def insert_detected_user_profile(self, record:DetectedUserProfile ) -> ObjectId:
        return self._insert_one(self.DETECTED_PROFILES_COLLECTION, record)

    def update_detected_user_profile(
            self,
            condition: Dict[str, Any],
            updated_profile_data: DetectedUserProfile
    ) -> UpdateResult:
        data_to_set = asdict(updated_profile_data)
        update_document = {"$set": data_to_set}
        return self._update_one(self.DETECTED_PROFILES_COLLECTION, condition, update_document)

    def get_detected_user_profile(self, condition: Dict[str, Any]) -> Optional[DetectedUserProfile]:
        doc = self._find_one(self.DETECTED_PROFILES_COLLECTION, condition)
        if doc:
            doc.pop("_id", None)
            try:
                return DetectedUserProfile(**doc)
            except TypeError as e:
                logger.error(f"Error creating FullUserProfile for doc {condition}: {e}. Document: {doc}")
                return None
        return None

    def get_detected_user_profiles(
        self,
        condition: Dict[str, Any],
        limit: int = 0,
        skip: int = 0,
        sort: Optional[List[Tuple[str, int]]] = None
    ) -> List[DetectedUserProfile]:
        docs = self._find_many(self.DETECTED_PROFILES_COLLECTION, condition, limit=limit, skip=skip, sort=sort)
        profiles: List[DetectedUserProfile] = []
        for doc in docs:
            doc.pop("_id", None)
            try:
                profiles.append(DetectedUserProfile(**doc))
            except TypeError as e:
                logger.error(f"Skipping doc due to TypeError: {e}. Document: {doc}")
                continue
        return profiles
db_interface = MongoDBInterface(db_name="WW-Telegram-Bot")
