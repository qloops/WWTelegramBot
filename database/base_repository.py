from typing import (
    TYPE_CHECKING,
    TypeVar, 
    Generic, 
    Type, 
    Optional, 
    List, 
    Dict, 
    Any, 
    Tuple
)
from dataclasses import asdict
from bson import ObjectId
from pymongo.results import UpdateResult
import logging

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from .database import MongoDBInterface

T = TypeVar("T")


class BaseRepository(Generic[T]):
    """
    Base repository class providing common database operations for entities.
    
    This class implements generic CRUD operations and query methods that can be
        inherited by specific repository implementations.
    
    Type Parameters:
        T: The model class type this repository manages.
    """
    
    def __init__(
            self, 
            db_interface: "MongoDBInterface", 
            collection_name: str, 
            model_class: Type[T]
    ):
        """
        Initialize the repository.

        Args:
            db_interface: MongoDB interface instance.
            collection_name: Name of the MongoDB collection.
            model_class: Model class for entity deserialization.
        """
        self._db = db_interface
        self._collection_name = collection_name
        self._model_class = model_class

    def insert_one(self, record: T) -> ObjectId:
        """
        Insert a single record into the collection.

        Args:
            record: Entity instance to insert.

        Returns:
            ObjectId: The inserted document's ID.
        """
        return self._db._insert_one(
            collection_name=self._collection_name, 
            record=record
        )

    def insert_many(self, records: List[T]) -> List[ObjectId]:
        """
        Insert multiple records into the collection.
        
        Args:
            records: List of entity instances to insert.
            
        Returns:
            List[ObjectId]: List of inserted document IDs.
        """
        return self._db._insert_many(
            collection_name=self._collection_name, 
            records=records
        )

    def update_one(self, condition: Dict[str, Any], record: T) -> UpdateResult:
        """
        Update a single document matching the condition.
        
        Args:
            condition: Query condition to find the document.
            record: Entity instance with updated values.
            
        Returns:
            UpdateResult: MongoDB update operation result.
        """
        data_to_set = asdict(record)
        update_document = {"$set": data_to_set}
        return self._db._update_one(
            collection_name=self._collection_name, 
            condition=condition, 
            update_operations=update_document
        )

    def update_many(self, condition: Dict[str, Any], record: T) -> UpdateResult:
        """
        Update multiple documents matching the condition.
        
        Args:
            condition: Query condition to find documents.
            record: Entity instance with updated values.
            
        Returns:
            UpdateResult: MongoDB update operation result.
        """
        data_to_set = asdict(record)
        update_document = {"$set": data_to_set}
        return self._db._update_many(
            collection_name=self._collection_name, 
            condition=condition, 
            update_operations=update_document
        )

    def update_field(
            self, 
            condition: Dict[str, Any], 
            field_name: str, 
            field_value: Any
    ) -> UpdateResult:
        """
        Update a specific field in document matching the condition.
        
        Args:
            condition: Query condition to find document.
            field_name: Name of the field to update.
            field_value: New value for the field.
            
        Returns:
            UpdateResult: MongoDB update operation result.
        """
        update_document = {"$set": {field_name: field_value}}
        return self._db._update_one(
            collection_name=self._collection_name, 
            condition=condition, 
            update_operations=update_document
        )

    def find_one(self, condition: Dict[str, Any]) -> Optional[T]:
        """
        Find a single document matching the condition.
        
        Args:
            condition: Query condition to find document.
            
        Returns:
            Optional[T]: Entity instance if found, None otherwise.
        """
        doc = self._db._find_one(
            collection_name=self._collection_name, 
            condition=condition, 
            projection={"_id": 0}
        )

        if doc:
            try:
                return self._model_class(**doc)
            except TypeError as e:
                logger.error(
                    f"Error creating {self._model_class.__name__} for condition"
                    f"{condition}: {e}. Document: {doc}.")
                return None
        return None

    def find_many(
        self, 
        condition: Dict[str, Any],
        limit: Optional[int] = 0,
        skip: int = 0,
        sort: Optional[List[Tuple[str, int]]] = None
    ) -> List[T]:
        """
        Find multiple documents matching the condition.
        
        Args:
            condition: Query condition to find documents.
            limit: Maximum number of documents to return (0 for no limit).
            skip: Number of documents to skip.
            sort: List of (field_name, sort_order) tuples for sorting.

        Returns:
            List[T]: List of entity instances.
        """
        docs = self._db._find_many(
            collection_name=self._collection_name, 
            condition=condition,
            projection={"_id": 0},
            limit=limit, 
            skip=skip,
            sort=sort
        )
        results = []
        for doc in docs:
            try:
                results.append(self._model_class(**doc))
            except TypeError as e:
                logger.error(
                    f"Skipping doc due to TypeError: {e}. Document: {doc}."
                )
                continue
        return results

    def find_all(self, limit: Optional[int] = 0, skip: int = 0) -> List[T]:
        """
        Find all documents in the collection.
        
        Args:
            limit: Maximum number of documents to return (0 for no limit).
            skip: Number of documents to skip.
            
        Returns:
            List[T]: List of all entity instances.
        """
        return self.find_many(
            condition={},
            limit=limit,
            skip=skip
        )

    def count(self, condition: Dict[str, Any] = {}) -> int:
        """
        Count documents matching the condition.

        Args:
            condition: Query condition (empty dict to count all documents).

        Returns:
            int: Number of matching documents.
        """
        collection = self._db._get_collection(self._collection_name)
        return collection.count_documents(filter=condition)

    def exists(self, condition: Dict[str, Any]) -> bool:
        """
        Check if any document matching the condition exists.
        
        Args:
            condition: Query condition to find document.
            
        Returns:
            bool: True if at least one document exists, False otherwise.
        """
        return self.count(condition) > 0