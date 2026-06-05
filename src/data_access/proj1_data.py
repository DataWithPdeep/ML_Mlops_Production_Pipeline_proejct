import sys
import pandas as pd
import numpy as np
from typing import Optional

from src.configuration.mongo_db_connection import MongoDBClient
from src.constants import DATABASE_NAME
from src.exception import MyException


class Proj1Data:

    def __init__(self) -> None:
        try:
            self.mongo_client = MongoDBClient(database_name=DATABASE_NAME)
        except Exception as e:
            raise MyException(e, sys)

    def export_collection_as_dataframe(
        self,
        collection_name: str,
        database_name: Optional[str] = None
    ) -> pd.DataFrame:

        try:
            if database_name is None:
                database_name = DATABASE_NAME

            collection = self.mongo_client.database[collection_name]

            print(f"Database: {database_name}")
            print(f"Collection: {collection_name}")

            # TEMPORARY TEST
            cursor = collection.find().limit(10000)
            df = pd.DataFrame(list(cursor))

            print(f"Data fetched successfully: {df.shape}")

            if "_id" in df.columns:
                df.drop("_id", axis=1, inplace=True)

            if "id" in df.columns:
                df.drop("id", axis=1, inplace=True)

            df.replace({"na": np.nan}, inplace=True)

            return df

        except Exception as e:
            raise MyException(e, sys)