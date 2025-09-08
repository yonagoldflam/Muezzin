from elasticsearch import Elasticsearch, helpers

class ElasticDal:
    def __init__(self, host="localhost", port=9200):
        self.client = Elasticsearch(hosts=[f'http://{host}:{port}'])

    def create_index(self, index_name):
        try:
            if not self.client.indices.exists(index=index_name):
                self.client.indices.create(index=index_name)

        except Exception as e:
            print(f'field to create index: {e}')

    def insert_document(self,index, document, doc_id):
        try:
            if not self.client.exists(index=index, id=doc_id):
                return self.client.index(index=index, body=document, id=doc_id)
            else:
                return 'id_document already exists'
        except Exception as e:
            print(f'field to insert {document} {e}')

    def delete_index(self, index_name):
        try:
            if self.client.indices.exists(index=index_name):
                self.client.indices.delete(index=index_name)
            else:
                return 'id_document does not exist'
        except Exception as e:
            print(f'field to delete index: {e}')
