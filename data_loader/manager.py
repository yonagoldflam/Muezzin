import time
from pathlib import Path
from utils.kafka_configuration import produce_message, send_event

class Manager:
    def __init__(self):
        self.directory_files_path = 'C:/podcasts'

    def run_files_and_publish_the_path_and_meta_data_to_kafka(self):
        producer = produce_message()
        topic = 'path_meta-data'
        path = Path(self.directory_files_path)
        for file in path.iterdir():
            document = self.create_json_file_with_path_and_meta_data(file)
            send_event(producer, topic, document)



    def create_json_file_with_path_and_meta_data(self,file : Path):
        meta_data = self.create_meta_data(file)
        document = {'file_path': str(file),
                    'meta_data': meta_data}
        return document

    def create_meta_data(self, file : Path):
        meta_data = {'name' : file.name,
                     'size' : file.stat().st_size,
                     'data_time' : time.ctime(file.stat().st_mtime)}

        return meta_data





if __name__ == '__main__':
    m = Manager()
    m.run_files_and_publish_the_path_and_meta_data_to_kafka()
