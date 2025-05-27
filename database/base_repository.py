from typing import TypeVar, Generic, Type, Optional, List, Dict, Any, Tuple
from dataclasses import asdict
from bson import ObjectId
from pymongo.results import UpdateResult
import logging

logger = logging.getLogger(__name__)

T = TypeVar("T")


class BaseRepository(Generic[T]):
    def __init__(self, db_interface: "MongoDBInterface", collection_name: str, model_class: Type[T]):
        self._db = db_interface
        self._collection_name = collection_name
        self._model_class = model_class
    
    def insert_one(self, record: T) -> ObjectId:
        return self._db._insert_one(self._collection_name, record)
    
    def insert_many(self, records: List[T]) -> List[ObjectId]:
        return self._db._insert_many(self._collection_name, records)
    
    def update_one(self, condition: Dict[str, Any], record: T) -> UpdateResult:
        data_to_set = asdict(record)
        update_document = {"$set": data_to_set}
        return self._db._update_one(self._collection_name, condition, update_document)
    
    def update_many(self, condition: Dict[str, Any], record: T) -> UpdateResult:
        data_to_set = asdict(record)
        update_document = {"$set": data_to_set}
        return self._db._update_many(self._collection_name, condition, update_document)

    def find_one(self, condition: Dict[str, Any]) -> Optional[T]:
        doc = self._db._find_one(self._collection_name, condition)
        if doc:
            doc.pop("_id", None)
            try:
                return self._model_class(**doc)
            except TypeError as e:
                logger.error(f"Error creating {self._model_class.__name__} for condition {condition}: {e}. Document: {doc}")
                return None
        return None
    
    def find_many(
        self, 
        condition: Dict[str, Any],
        limit: int = 0,
        skip: int = 0,
        sort: Optional[List[Tuple[str, int]]] = None
    ) -> List[T]:
        docs = self._db._find_many(
            self._collection_name, 
            condition, 
            limit=limit, 
            skip=skip, 
            sort=sort
        )
        results = []
        for doc in docs:
            doc.pop("_id", None)
            try:
                results.append(self._model_class(**doc))
            except TypeError as e:
                logger.error(f"Skipping doc due to TypeError: {e}. Document: {doc}")
                continue
        return results
    
    def find_all(self, limit: int = 0, skip: int = 0) -> List[T]:
        return self.find_many({}, limit=limit, skip=skip)

    def count(self, condition: Dict[str, Any] = {}) -> int:
        collection = self._db._get_collection(self._collection_name)
        return collection.count_documents(condition)
    
    def exists(self, condition: Dict[str, Any]) -> bool:
        return self.find_one(condition) is not None