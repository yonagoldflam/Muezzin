from utils.elastic_search.elastic_dal import ElasticDal
from text_decoding import TextDecoding
from utils.kafka_configuration.kafka_configuration import consume_messages
from utils.logging.logger import Logger

logger = Logger().get_logger()

class Manager:
    def __init__(self):
        self.text_decoding = TextDecoding()
        self.hostile_encoding = 'R2Vub2NpZGUsV2FyIENyaW1lcyxBcGFydGhlaWQsTWFzc2FjcmUsTmFrYmEsRGlzcGxhY2VtZW50LEh1bWFuaXRhcmlhbiBDcmlzaXMsQmxvY2thZGUsT2NjdXBhdGlvbixSZWZ1Z2VlcyxJQ0MsQkRT'
        self.not_hostile_encoding = 'RnJlZWRvbSBGbG90aWxsYSxSZXNpc3RhbmNlLExpYmVyYXRpb24sRnJlZSBQYWxlc3RpbmUsR2F6YSxDZWFzZWZpcmUsUHJvdGVzdCxVTlJXQQ=='
        self.hostile_decoding_list = self.decode(self.hostile_encoding)
        self.not_hostile_decoding_list = self.decode(self.not_hostile_encoding)
        self.elastic_client = ElasticDal()
        self.index = 'muezzin_podcasts'


    def decode(self, encoded_string):
        decoded_string = self.text_decoding.decode_base64(encoded_string)
        decoded_list = decoded_string.lower().split(',')
        return decoded_list

    def main(self):
        topic = 'muezzin_text'
        consumer = consume_messages(topic)
        for event in consumer:
            document = event.value
            doc_id = document['id']
            text = document['text'].lower()
            score = self.calculate_hostile_score(text)
            self.add_bds_field_to_document(doc_id, score)
            self.add_threat_level_field(doc_id, score)


    def add_bds_field_to_document(self, doc_id,score):
        bds_field = self.is_bds(score)
        self.elastic_client.add_field_to_document(self.index, doc_id, bds_field)
        logger.info(f'field {bds_field} added to doc id:{doc_id} in elastic')

    def add_threat_level_field(self, doc_id, score):
        threat_level_field = self.threat_level_field(score)
        self.elastic_client.add_field_to_document(self.index, doc_id, threat_level_field)
        logger.info(f'field {threat_level_field} added to doc id:{doc_id} in elastic')


    def calculate_hostile_score(self, text):
        score = 0
        for hostile in self.hostile_decoding_list:
            score += text.count(hostile) * 2
        for not_hostile in self.not_hostile_decoding_list:
            score += text.count(not_hostile)
        if score:
            return len(text) / score
        return 0

    def is_bds(self, score):
        is_bds_field = {'is_bds': 'True'}
        not_bds_field = {'is_bds': 'False'}
        if score:
            if score < 60:
                return is_bds_field
            else:
                return not_bds_field
        return not_bds_field

    def threat_level_field(self, score):
        high_threat_field = {'bds_threat_level': 'high'}
        medium_threat_field = {'bds_threat_level': 'medium'}
        none_threat_field = {'bds_threat_level': 'none'}
        if score < 40:
            return high_threat_field
        elif score < 100:
            return medium_threat_field
        else:
            return none_threat_field

if __name__ == '__main__':
    manager = Manager()
    manager.main()


