from utils.kafka_configuration import consume_messages
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
        mongo_connection = Connection()
        self.mongo_db = MongoDal(mongo_connection)
        self.collection_name = 'muezzin_podcasts'


    def consume_hash_insert_to_elastic_and_mongo(self):
        topic = 'path_meta-data'
        consumer = consume_messages(topic)
        for event in consumer:
            self.splitter_event_to_meta_data_and_path_and_storaging(event)

    def splitter_event_to_meta_data_and_path_and_storaging(self, event):
        document = event.value
        file_path = document['file_path']
        meta_data = document['meta_data']
        meta_data_hashed = self.create_hash(meta_data)
        self.elastic_client.insert_document(index=self.index_name, document=meta_data, doc_id=meta_data_hashed)
        binary_audio_with_id = self.create_document_with_id_and_binary_audio_file(meta_data_hashed, file_path)
        if not self.mongo_db.find_one(collection_name=self.collection_name, query={'_id': meta_data_hashed}):
            self.mongo_db.insert_one(collection_name=self.collection_name, document=binary_audio_with_id)

    def create_document_with_id_and_binary_audio_file(self, doc_id, file_path):
        binary_audio = self.read_wav_file(file_path)
        document_with_id_and_binary_audio_file = {'_id': doc_id, 'audio': binary_audio}
        return document_with_id_and_binary_audio_file


    def create_hash(self, document):
        sort_document = json.dumps(document, sort_keys=True).encode('utf-8')
        hashed_document = hashlib.sha256(sort_document).hexdigest()
        return hashed_document


    def read_wav_file(self, path):
        with open(path, 'rb') as f:
            return f.read()

elastic_client = ElasticDal()
if __name__ == '__main__':
    manager = Manager()
    elastic_client.delete_index(index_name='meta_data_podcasts')
    manager.consume_hash_insert_to_elastic_and_mongo()