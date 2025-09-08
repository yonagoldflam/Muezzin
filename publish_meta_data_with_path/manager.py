import time
from pathlib import Path
from utils.kafka_configuration import produce_message, send_event
from utils.logging.logger import Logger

logger = Logger().get_logger()


class Manager:
    def __init__(self):
        logger.info('initializing publish meta data with path manager')
        self.directory_files_path = 'C:/podcasts'
        self.path = Path(self.directory_files_path)
        logger.info(f'pathing: {self.path} successful')
        self.producer = produce_message()
        self.topic = 'path_meta-data'

    def run_files_and_publish_the_path_and_meta_data_to_kafka(self):
        for file in self.path.iterdir():
            document = self.create_json_file_with_path_and_meta_data(file)
            send_event(self.producer, self.topic, document)



    def create_json_file_with_path_and_meta_data(self, file : Path):
        meta_data = self.create_meta_data(file)
        document = {'file_path': str(file),
                    'meta_data': meta_data}

        if document['file_path'] and document['meta_data']:
            logger.info(f'creating json file: {document} successful')
        else:
            logger.error(f'creating json file: {document} failed')
        return document

    def create_meta_data(self, file : Path):
        meta_data = {'name' : file.name,
                     'size' : file.stat().st_size,
                     'data_time' : time.ctime(file.stat().st_ctime)}

        if meta_data['name'] and meta_data['size'] and meta_data['date_time']:
            logger.info(f'creating meta data: {meta_data} successful')
        else:
            logger.error(f'creating meta data: {meta_data} failed')

        return meta_data

if __name__ == '__main__':
    m = Manager()
    m.run_files_and_publish_the_path_and_meta_data_to_kafka()
