from utils.elastic_search.elastic_dal import ElasticDal
from text_decoding import TextDecoding

class Manager:
    def __init__(self):
        self.text_decoding = TextDecoding()
        self.hostile_encoding = 'R2Vub2NpZGUsV2FyIENyaW1lcyxBcGFydGhlaWQsTWFzc2FjcmUsTmFrYmEsRGlzcGxhY2VtZW50LEh1bWFuaXRhcmlhbiBDcmlzaXMsQmxvY2thZGUsT2NjdXBhdGlvbixSZWZ1Z2VlcyxJQ0MsQkRT'
        self.not_hostile_encoding = 'RnJlZWRvbSBGbG90aWxsYSxSZXNpc3RhbmNlLExpYmVyYXRpb24sRnJlZSBQYWxlc3RpbmUsR2F6YSxDZWFzZWZpcmUsUHJvdGVzdCxVTlJXQQ=='
        self.hostile_decoding_list = self.decode(self.hostile_encoding)
        self.not_hostile_decoding_list = self.decode(self.not_hostile_encoding)

    def decode(self, encoded_string):
        decoded_string = self.text_decoding.decode_base64(encoded_string)
        decoded_list = decoded_string.split(',')
        return decoded_list

if __name__ == '__main__':
    manager = Manager()
    print(manager.hostile_decoding_list)
    print(manager.not_hostile_decoding_list)
