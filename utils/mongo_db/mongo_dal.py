

class MongoDal:
    def __init__(self, connection):
        self.connection = connection

    def insert_one(self, collection_name, document):
        self.connection.db[collection_name].insert_one(document)

    def insert_many(self, collection_name, documents):
        return self.connection.db[collection_name].insert_many(documents)

    def find(self, collection_name, query):
        return self.connection.db[collection_name].find(query)

    def find_one(self, collection_name, query):
        return self.connection.db[collection_name].find_one(query)

    def find_all(self, collection_name):
        return list(self.connection.db[collection_name].find())

a = MongoDal