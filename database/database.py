import logging
import os
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
    """
    Interface for MongoDB database operations.
    
    Provides low-level database operations and manages repository instances
    for different collections.
    """
    
    _client: MongoClient
    _db: Database
    
    # Repositories
    users: UserRepository
    users_settings: UserSettingsRepository
    users_profiles: UserProfileRepository
    media_cache: MediaCacheRepository

    def __init__(self, db_name: str, host: str = "localhost", port: int = 27017) -> None:
        """
        Initialize MongoDB connection and repositories.
        
        Args:
            db_name: Name of the database to connect to
            host: MongoDB server host
            port: MongoDB server port
            
        Raises:
            ConnectionFailure: If connection to MongoDB fails
            Exception: If any other error occurs during initialization
        """
        try:
            self._client = MongoClient(host, port, serverSelectionTimeoutMS=5000)
            self._db = self._client[db_name]
            self._db.command("ping")
            
            logger.info(f"Successfully connected to MongoDB at {host}:{port}, database: {db_name}")
            
            self._init_repositories()
            
        except ConnectionFailure as e:
            raise ConnectionFailure(f"Could not connect to MongoDB at {host}:{port}: {e}")
        except Exception as e:
            if hasattr(self, '_client'):
                self._client.close()
            raise Exception(f"An unexpected error occurred during MongoDB connection: {e}")
    
    def _init_repositories(self) -> None:
        """Initialize repository instances."""
        self.users = UserRepository(self)
        self.users_settings = UserSettingsRepository(self)
        self.users_profiles = UserProfileRepository(self)
        self.media_cache = MediaCacheRepository(self)

    def _get_collection(self, collection_name: str) -> Collection:
        """
        Get a collection by name.
        
        Args:
            collection_name: Name of the collection
            
        Returns:
            Collection: MongoDB collection instance
        """
        return self._db[collection_name]

    def _insert_one(self, collection_name: str, record: Any) -> ObjectId:
        """
        Insert a single document into a collection.
        
        Args:
            collection_name: Name of the collection
            record: Dataclass instance to insert
            
        Returns:
            ObjectId: ID of the inserted document
        """
        collection = self._get_collection(collection_name)
        document_to_insert = asdict(record)
        result = collection.insert_one(document_to_insert)
        return result.inserted_id

    def _insert_many(self, collection_name: str, records: List[Any]) -> List[ObjectId]:
        """
        Insert multiple documents into a collection.
        
        Args:
            collection_name: Name of the collection
            records: List of dataclass instances to insert
            
        Returns:
            List[ObjectId]: List of IDs of inserted documents
        """
        collection = self._get_collection(collection_name)
        documents_to_insert = [asdict(r) for r in records]
        result = collection.insert_many(documents_to_insert)
        return result.inserted_ids

    def _update_one(
        self, 
        collection_name: str, 
        condition: Dict[str, Any], 
        update_operations: Dict[str, Any]
    ) -> UpdateResult:
        """
        Update a single document in a collection.
        
        Args:
            collection_name: Name of the collection
            condition: Query condition to find the document
            update_operations: MongoDB update operations
            
        Returns:
            UpdateResult: Result of the update operation
        """
        collection = self._get_collection(collection_name)
        return collection.update_one(condition, update_operations)

    def _update_many(
        self,
        collection_name: str,
        condition: Dict[str, Any],
        update_operations: Dict[str, Any]
    ) -> UpdateResult:
        """
        Update multiple documents in a collection.
        
        Args:
            collection_name: Name of the collection
            condition: Query condition to find documents
            update_operations: MongoDB update operations
            
        Returns:
            UpdateResult: Result of the update operation
        """
        collection = self._get_collection(collection_name)
        return collection.update_many(condition, update_operations)

    def _find_one(
        self,
        collection_name: str,
        condition: Dict[str, Any],
        projection: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Find a single document in a collection.
        
        Args:
            collection_name: Name of the collection
            condition: Query condition
            projection: Fields to include/exclude in the result
            
        Returns:
            Optional[Dict[str, Any]]: Found document or None
        """
        collection = self._get_collection(collection_name)
        return collection.find_one(filter=condition, projection=projection)

    def _find_many(
        self,
        collection_name: str,
        condition: Dict[str, Any],
        projection: Optional[Dict[str, Any]] = None,
        limit: int = 0, 
        skip: int = 0,
        sort: Optional[List[Tuple[str, int]]] = None
    ) -> List[Dict[str, Any]]:
        """
        Find multiple documents in a collection.
        
        Args:
            collection_name: Name of the collection
            condition: Query condition
            projection: Fields to include/exclude in results
            limit: Maximum number of documents to return (0 for no limit)
            skip: Number of documents to skip
            sort: List of (field, direction) tuples for sorting
            
        Returns:
            List[Dict[str, Any]]: List of found documents
        """
        collection = self._get_collection(collection_name)
        cursor: Cursor = collection.find(filter=condition, projection=projection)
        
        if sort:
            cursor = cursor.sort(sort)
        if skip > 0:
            cursor = cursor.skip(skip)
        if limit > 0:
            cursor = cursor.limit(limit)

        return list(cursor)


class _LazyDBInterface:
    """
    Lazy wrapper for MongoDBInterface that creates connection on first access.
    
    This class delays the database connection until it's actually needed,
    preventing connection at import time.
    """

    # Repositories
    users: UserRepository
    users_settings: UserSettingsRepository
    users_profiles: UserProfileRepository
    media_cache: MediaCacheRepository

    def __init__(self):
        self._db: Optional[MongoDBInterface] = None
    
    def _ensure_connected(self) -> None:
        """
        Create database connection if not already connected.
        
        Raises:
            ValueError: If environment variables contain invalid values
            ConnectionFailure: If connection to MongoDB fails
        """
        if self._db is None:
            db_name = os.getenv("DB_NAME", "WW-Telegram-Bot")
            host = os.getenv("DB_HOST", "localhost")
            
            port = int(os.getenv("DB_PORT", 27017))

            logger.info(f"Initializing MongoDB connection to {host}:{port}, database: {db_name}")
            self._db = MongoDBInterface(db_name=db_name, host=host, port=port)
    
    def __getattr__(self, name: str) -> Any:
        """
        Delegate attribute access to the actual MongoDBInterface instance.
        
        Args:
            name: Attribute name to access
            
        Returns:
            Any: Attribute value from the MongoDBInterface instance
        """
        self._ensure_connected()
        return getattr(self._db, name)


db_interface = _LazyDBInterface()