from typing import Optional, List, Any
from bson import ObjectId
from dataclasses import asdict 

from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from pymongo.errors import ConnectionFailure

from .models import FullUserProfile


class MongoDBInterface:
    client: Optional[MongoClient]
    _db: Optional[Database]

    def __init__(self,  db_name: str, host: str = "localhost", port: int = 27017) -> None:
        self.client = None
        self._db = None
        
        try:
            self.client = MongoClient(host, port)
            
            self._db = self.client[db_name]
            self._db.command("ping")
        except ConnectionFailure as e:
            if self.client:
                self.client.close()
            raise ConnectionFailure(f"Could not connect to MongoDB at {host}:{port}: {e}")
        except Exception as e:
            if self.client:
                self.client.close()
            raise Exception(f"An unexpected error occurred during MongoDB connection: {e}")

    def _get_collection(self, collection_name: str) -> Collection:
        return self._db[collection_name]
    # TODO Перечислить в анотации recrord dataclass, которые они могут принимать. 
    def _insert_one(self, collection_name: str, record: Any) -> ObjectId:
        collection = self._get_collection(collection_name)
        document_to_insert = asdict(record)
        result = collection.insert_one(document_to_insert)
        return result.inserted_id

    def _insert_many(self, collection_name: str, records: List[Any]) -> List[ObjectId]:
        collection = self._get_collection(collection_name)
        documents_to_insert = [asdict(record) for record in records]
        result = collection.insert_many(documents_to_insert)
        return result.inserted_ids

    def insert_profile(self, records: FullUserProfile):
        self._insert_many("users_profiles", records)

db_interface = MongoDBInterface(db_name="WW-Telegram-Bot")
