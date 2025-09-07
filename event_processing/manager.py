from utils.kafka_configuration import consume_message
import hashlib
import json

class Manager:
    def __init__(self):
        pass



    def create_hash(self, document):
        sort_document = json.dumps(document, sort_keys=True).encode('utf-8')
        hashed_document = hashlib.sha256(sort_document).hexdigest()
        return hash



