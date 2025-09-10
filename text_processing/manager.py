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
        self.dangerous_score = {'id':{'hostile':0, 'not hostile':0}}

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
            final_score = len(text) / score





if __name__ == '__main__':
    manager = Manager()
    score = 0
    document = " The news cycle moves fast, but Gaza doesn't disappear when cameras do. The blockade is still there, and so is the humanitarian crisis. Exactly. I read a report yesterday. It said malnutrition is spreading among children. That's a war crime in itself. Meanwhile, refugees keep growing in number, and displacement means whole communities are erased. The protests worldwide are encouraging, though. From London to New York, people chant for a ceasefire and free Palestine. And linking it back to BDS, it's about applying pressure where governments fail. Right. Liberation isn't easy, but the people's resilience is inspiring. Resistance can be cultural, political, and global. And podcasts like ours? Just small ripples. But ripples matter."
    text = document
    for hostile in manager.hostile_decoding_list:
        score += text.count(hostile) * 2
    for not_hostile in manager.not_hostile_decoding_list:
        score += text.count(not_hostile)
    print(score)
    score = len(text) / score
    print(score)
    score = 0
    text = " behind every statistic is a human story. Refugees aren't numbers, they're families. Exactly. I spoke to a volunteer who said the displacement is relentless, shelters overflow, and yet the blockade tightens. And the ICC documents war crimes, but children still die waiting for medicine. That's why activism matters. Boycotts, protests, solidarity, small actions, big meaning. Free Palestine isn't just police. It's humanitarian, and every voice counts in ending genocide."
    for hostile in manager.hostile_decoding_list:
        score += text.count(hostile) * 2
    for not_hostile in manager.not_hostile_decoding_list:
        score += text.count(not_hostile)
    print(score)
    score = len(text) / score
    print(score)


