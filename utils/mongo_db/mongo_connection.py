import os
import pymongo
from pymongo.errors import PyMongoError
from utils.logging.logger import Logger

logger = Logger().get_logger()

class Connection:
    def __init__(self):
        try:
            mongo_user = os.getenv('MONGO_USER', 'shneyor')
            mongo_password = os.getenv('MONGO_PASSWORD', 'zalmen')
            mongo_db = os.getenv('MONGO_DB', 'muezzin_db')
            mongo_host = os.getenv('MONGO_HOST', 'localhost')
            mongo_port = os.getenv('MONGO_PORT', '27017')
            auth_db = os.getenv('MONGO_AUTH_DB','admin')

            self.client = pymongo.MongoClient(
                host=mongo_host,
                port=int(mongo_port),
                username=mongo_user,
                password=mongo_password,
                authSource=auth_db,
            )

            self.db = self.client[mongo_db]
            logger.info(f'connected to mongo db: {mongo_db} successful')

        except PyMongoError as e:
            logger.info(f'failed to connect to mongo db with error: {e}')
            raise RuntimeError