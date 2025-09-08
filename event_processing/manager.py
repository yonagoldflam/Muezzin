from utils.kafka_configuration import consume_message
from utils.elastic_search.elastic_dal import ElasticDal
from utils.mongo_db.mongo_connection import Connection
from utils.mongo_db.mongo_dal import MongoDal
import hashlib
import json

class Manager:
    def __init__(self):
        self.elastic_client = ElasticDal()
        self.index_name = 'meta_data_podcasts'
        self.elastic_client.create_index(self.index_name)
        connection = Connection()
        self.mongo_d = MongoDal(connection)
        self.collection_name = 'muezzin_podcasts'


    def consume_hash_and_insert_to_elastic(self):
        topic = 'path_meta-data'
        consumer = consume_message(topic)
        for message in consumer:
            document = message.value
            path_file = document['file_path']
            meta_data = document['meta_data']
            meta_data_hashed = self.create_hash(meta_data)
            self.elastic_client.insert_document(index=self.index_name, document=meta_data, doc_id=meta_data_hashed)
            binary_audio = self.read_wav_file(path_file)
            binary_audio_with_id = {'_id': meta_data_hashed, 'audio': binary_audio}
            if not self.mongo_d.find_one(collection_name=self.collection_name, query={'_id': meta_data_hashed}):
                self.mongo_d.insert_one(collection_name=self.collection_name, document=binary_audio_with_id)



    def create_hash(self, document):
        sort_document = json.dumps(document, sort_keys=True).encode('utf-8')
        hashed_document = hashlib.sha256(sort_document).hexdigest()
        return hashed_document

    def read_wav_file(self, path):
        with open(path, 'rb') as f:
            return f.read()



if __name__ == '__main__':
    manager = Manager()
    manager.elastic_client.delete_index(index_name=manager.index_name)
    manager.consume_hash_and_insert_to_elastic()