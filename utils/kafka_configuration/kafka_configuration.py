import json
import os
from kafka import KafkaProducer, KafkaConsumer
from utils.logging.logger import Logger

logger = Logger().get_logger()

kafka_broker = os.getenv('KAFKA_BROKER', 'kafka:9092')

def produce_message():
    try:
        produce = KafkaProducer(bootstrap_servers=[kafka_broker],
                                 value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        logger.info(f'kafka connection successful')
        return produce
    except Exception as e:
        logger.error(f'failed to produce message: {e}')
        raise
def send_event(produce, topic, event):
    try:
        produce.send(topic, event)
        produce.flush()
        logger.info(f'kafka sent event successful')
    except Exception as e:
        logger.error(f'failed to send event:{event} error: {e}')

def consume_messages(*topics):
    try:
        consumer = KafkaConsumer(*topics,
                                 group_id='my-group',
                                 value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                                 bootstrap_servers=[kafka_broker],
                                 auto_offset_reset='earliest'
                                 )
        logger.info(f'kafka consume messages successful')
        return consumer
    except Exception as e:
        logger.error(f'failed to consume messages: {e}')
        raise