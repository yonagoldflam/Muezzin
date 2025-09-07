import json
import os
from kafka import KafkaProducer, KafkaConsumer

kafka_broker = os.getenv('KAFKA_BROKER', 'kafka-broker:9092')

def produce_message():
    try:
        produce = KafkaProducer(bootstrap_servers=[kafka_broker],
                                 value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        return produce
    except Exception as e:
        raise RuntimeError(f'Failed to produce message: {e}')

def send_event(produce, topic, event):
    produce.send(topic, event)
    produce.flush()

def consume_message(*topics):
    try:
        consumer = KafkaConsumer(*topics,
                                 group_id='my-group',
                                 value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                                 bootstrap_servers=[kafka_broker],
                                 auto_offset_reset='earliest'
                                 )

        return consumer
    except Exception as e:
        raise RuntimeError(f'Failed to consume message: {e}')