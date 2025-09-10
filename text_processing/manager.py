from sympy.polys.subresultants_qq_zz import final_touches

from utils.elastic_search.elastic_dal import ElasticDal
from text_decoding import TextDecoding
from utils.kafka_configuration import consume_messages

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
            score = 0
            document = event.value
            text = document['text']
            for hostile in self.hostile_decoding_list:
                score += text.count(hostile) * 2
            for not_hostile in self.not_hostile_decoding_list:
                score += text.count(not_hostile)
            if score:
                final_score = len(text) / score
            else:
                final_score = 0
            if final_score > 60:
                new_field = {'is_bds': 'True'}
            else:
                new_field = {'is_bds': 'False'}
            doc_id = document['id']
            self.elastic_client.add_field_to_document(self.index, doc_id, new_field)






if __name__ == '__main__':
    manager = Manager()
    manager.main()


