from utils.kafka_configuration import consume_messages
from utils.elastic_search.elastic_dal import ElasticDal
from utils.mongo_db.mongo_connection import Connection
from utils.mongo_db.mongo_dal import MongoDal
import hashlib
import json
from utils.logging.logger import Logger
from transcription_audio import Transcriber

logger = Logger().get_logger()

class Manager:
    def __init__(self):
        logger.info("'event processing' manager start")
        self.elastic_client = ElasticDal()
        self.index_name = 'muezzin_podcasts'
        self.elastic_client.create_index(self.index_name)
        mongo_connection = Connection()
        self.mongo_db = MongoDal(mongo_connection)
        self.collection_name = 'muezzin_podcasts'

        self.model_name = 'distil-large-v3'
        self.device = 'cpu'
        self.computer_type = 'int8'
        self.language = 'en'
        self.converter = Transcriber(model_name=self.model_name, device=self.device,
                                     computer_type=self.computer_type, language=self.language)


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
        self.build_podcast_document_transcription_insert_elastic(meta_data, meta_data_hashed, file_path)
        binary_audio_with_id = self.create_document_with_id_and_binary_audio_file(meta_data_hashed, file_path)
        if not self.mongo_db.check_id_is_exists(self.collection_name, meta_data_hashed):
            self.mongo_db.insert_one(self.collection_name, binary_audio_with_id)

    def build_podcast_document_transcription_insert_elastic(self, meta_data, doc_id, file_path):
        text = self.converter.transcribe(file_path)
        meta_data['text'] = text
        self.elastic_client.insert_document(index=self.index_name, document=meta_data, doc_id=doc_id)

    def create_document_with_id_and_binary_audio_file(self, doc_id, file_path):
        binary_audio = self.read_wav_file(file_path)
        document_with_id_and_binary_audio_file = {'_id': doc_id, 'audio': binary_audio}
        logger.info(f'created document with id and binary audio successful.')
        return document_with_id_and_binary_audio_file


    def create_hash(self, document):
        sort_document = json.dumps(document, sort_keys=True).encode('utf-8')
        hashed_document = hashlib.sha256(sort_document).hexdigest()
        logger.info(f'hash successful. document: {document}')
        return hashed_document

    def read_wav_file(self, path):
        try:
            with open(path, 'rb') as f:
                binary_audio_file = f.read()
                logger.info(f'read audio file successful')
                return binary_audio_file
        except Exception as e:
            logger.error(f'read audio file failed. with error: {e}')

elastic_client = ElasticDal()
if __name__ == '__main__':
    manager = Manager()
    elastic_client.delete_index(index_name='meta_data_podcasts')
    manager.consume_hash_insert_to_elastic_and_mongo()