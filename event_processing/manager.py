from utils.kafka_configuration import consume_message
from utils.elastic_search.elastic_dal import ElasticDal
import hashlib
import json

class Manager:
    def __init__(self):
        self.elastic_client = ElasticDal()
        self.index_name = 'meta_data_podcasts'
        self.elastic_client.create_index(self.index_name)

    def consume_hash_and_insert_to_elastic(self):
        topic = 'path_meta-data'
        consumer = consume_message(topic)
        for message in consumer:
            document = message.value
            path_file = document['file_path']
            meta_data = document['meta_data']
            hashed = self.create_hash(meta_data)
            self.elastic_client.insert_document(self.index_name, meta_data ,hashed)

    def create_hash(self, document):
        sort_document = json.dumps(document, sort_keys=True).encode('utf-8')
        hashed_document = hashlib.sha256(sort_document).hexdigest()
        return hashed_document


if __name__ == '__main__':
    manager = Manager()
    manager.consume_hash_and_insert_to_elastic()