from utils.logging.logger import Logger

logger = Logger().get_logger()

class MongoDal:
    def __init__(self, connection):
        self.connection = connection

    def insert_one(self, collection_name, document):
        try:
            self.connection.db[collection_name].insert_one(document)
            logger.info(f'insert document successful')
        except Exception as e:
            logger.error(f'insert document error with: {e}')

    def insert_many(self, collection_name, documents):
        try:
            self.connection.db[collection_name].insert_many(documents)
            logger.info(f'insert documents successful')
        except Exception as e:
            logger.error(f'insert documents error with: {e}')

    def find(self, collection_name, query):
        try:
            documents = self.connection.db[collection_name].find(query)
            logger.info(f'find documents successful')
            return documents
        except Exception as e:
            logger.error(f'find documents error with: {e}')

    def find_one(self, collection_name, query):
        try:
            documents = self.connection.db[collection_name].find_one(query)
            logger.info(f'find document successful')
            return documents
        except Exception as e:
            logger.error(f'find document error with: {e}')

    def find_all(self, collection_name):
        try:
            documents = list(self.connection.db[collection_name].find())
            logger.info(f'find all documents successful')
            return documents
        except Exception as e:
            logger.error(f'find all documents error with: {e}')

