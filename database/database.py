from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from pymongo.errors import ConnectionFailure
from typing import Optional, Mapping, List, Any
from bson import ObjectId


class MongoDBInterface:
    client: Optional[MongoClient]
    db: Optional[Database]

    def __init__(self,  db_name: str, host: str = "localhost", port: int = 27017) -> None:
        self.client = None
        self._db = None
        
        try:
            self.client = MongoClient(host, port)
            
            self._db = self.client[db_name]
            self._db.command("ping")
        except ConnectionFailure as e:
            raise ConnectionFailure(f"Could not connect to MongoDB at {host}:{port}: {e}")
        except Exception as e:
            raise Exception(f"An unexpected error occurred during MongoDB connection: {e}")

    def _get_collection(self, collection_name: str) -> Collection:
        return self._db[collection_name]

    def _insert_one(self, collection_name: str, document: Mapping[str, Any]) -> ObjectId:
        collection = self._get_collection(collection_name)
        result = collection.insert_one(document)
        return result.inserted_id

    def _insert_many(self, collection_name: str, documents: List[Mapping[str, Any]]) -> List[ObjectId]:
        collection = self._get_collection(collection_name)
        result = collection.insert_many(documents)
        return result.inserted_ids


db_interface: MongoDBInterface = MongoDBInterface("test")
