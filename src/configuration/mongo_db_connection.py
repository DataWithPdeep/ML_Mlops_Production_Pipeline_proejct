import os
import sys
import ssl
import pymongo
import certifi

from src.exception import MyException
from src.logger import logging
from src.constants import DATABASE_NAME, MONGODB_URL_KEY


class MongoDBClient:
    client = None

    def __init__(self, database_name: str = DATABASE_NAME) -> None:
        try:
            if MongoDBClient.client is None:
                mongo_db_url = os.getenv(MONGODB_URL_KEY)

                if mongo_db_url is None:
                    raise Exception(
                        f"Environment variable '{MONGODB_URL_KEY}' is not set."
                    )

                # SSL context manually banao
                ssl_context = ssl.create_default_context(
                    cafile=certifi.where()
                )
                ssl_context.check_hostname = True
                ssl_context.verify_mode = ssl.CERT_REQUIRED

                MongoDBClient.client = pymongo.MongoClient(
                    mongo_db_url,
                    tls=True,
                    tlsCAFile=certifi.where(),
                    serverSelectionTimeoutMS=30000,  # 300000 se kam karo
                    connectTimeoutMS=30000,
                    socketTimeoutMS=30000,
                )

                MongoDBClient.client.admin.command("ping")

            self.client = MongoDBClient.client
            self.database = self.client[database_name]
            self.database_name = database_name

            logging.info(f"MongoDB connection successful.\nDatabase: {database_name}")

        except Exception as e:
            raise MyException(e, sys)