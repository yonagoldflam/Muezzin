from elasticsearch import Elasticsearch, helpers

class ElasticDal:
    def __init__(self, host="localhost", port=9200):
        self.client = Elasticsearch(hosts=[f'http://{host}:{port}'])

    def create_index(self, index_name):
        try:
            self.client.indices.create(index=index_name)
        except Exception as e:
            print(f'field to create index: {e}')

    def insert_document(self,index, document):
        try:
            return self.client.index(index=index, body=document)
        except Exception as e:
            print(f'field to insert {document} {e}')