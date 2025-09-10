from utils.logging.logger import Logger

logger = Logger().get_logger()

class MongoDal:
    def __init__(self, connection):
        self.connection = connection

    def check_id_is_exists(self, collection_name ,doc_id):
        if self.find_one(collection_name=collection_name, query={'_id': doc_id}):
            logger.error(f'error: document id :{doc_id} already exists in collection: {collection_name} in mongo')
            return True
        else:
            return False

    def insert_one(self, collection_name, document):
        try:
            self.connection.db[collection_name].insert_one(document)
        except Exception as e:
            logger.error(f'insert document to mongo error with: {e}')

    def insert_many(self, collection_name, documents):
        try:
            self.connection.db[collection_name].insert_many(documents)
        except Exception as e:
            logger.error(f'insert documents to mongo error with: {e}')

    def find(self, collection_name, query):
        try:
            documents = self.connection.db[collection_name].find(query)
            return documents
        except Exception as e:
            logger.error(f'find documents in mongo error with: {e}')

    def find_one(self, collection_name, query):
        try:
            documents = self.connection.db[collection_name].find_one(query)
            return documents
        except Exception as e:
            logger.error(f'find document in mongo error with: {e}')

    def find_all(self, collection_name):
        try:
            documents = list(self.connection.db[collection_name].find())
            return documents
        except Exception as e:
            logger.error(f'find all documents in mongo error with: {e}')

    def find_by_id(self, collection_name, doc_id):
        try:
            return self.connection.db[collection_name].find_one({"_id": doc_id})
        except Exception as e:
            logger.error(f'find document id in mongo error with: {e}')


