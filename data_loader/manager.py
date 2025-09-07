from data_loader import DataLoader
from utils.kafka_configuration import produce_message, send_event

class Manager:
    def __init__(self):
        self.directory_files_path = 'C:/podcasts'
        self.data_loader = DataLoader(self.directory_files_path)

    def get_meta_data(self):
        return self.data_loader.meta_data()

    def publish_message(self):
        list_files = self.get_meta_data()
        producer = produce_message()
        topic = 'path_meta-data'
        for document in list_files:
            send_event(producer, topic, document)



if __name__ == '__main__':
    m = Manager()
    m.publish_message()
