from elasticsearch import Elasticsearch, helpers

from utils.logging.logger import Logger

logger = Logger().get_logger()

class ElasticDal:
    def __init__(self, host="localhost", port=9200):
        self.client = Elasticsearch(hosts=[f'http://{host}:{port}'])
        logger.info('connected to elasticsearch')


    def create_index(self, index_name):
        try:
            if not self.client.indices.exists(index=index_name):
                response = self.client.indices.create(index=index_name)
                if not response['acknowledged']:
                    logger.error(f'created index: {index_name} failed')
            else:
                logger.error(f'index: {index_name} already exists')

        except Exception as e:
            logger.error(f'field to create index: {e}')

    def insert_document(self,index, document, doc_id):
        try:
            if not self.client.exists(index=index, id=doc_id):
                response = self.client.index(index=index, body=document, id=doc_id)
                if not response['result'] == 'created':
                    logger.error(f'inserted to elastic document: {doc_id} failed')
            else:
                logger.error(f'document {doc_id} already exists in index: {index}')
        except Exception as e:
            logger.error(f'field insert to elastic document: {document} with error: {e}')

    def delete_index(self, index_name):
        try:
            if self.client.indices.exists(index=index_name):
                response = self.client.indices.delete(index=index_name)
                if not response['acknowledged']:
                    logger.error(f'deleted index: {index_name} from elastic failed')
            else:
                logger.error(f'index: {index_name} does not exist in elastic')
        except Exception as e:
            logger.error(f'field to delete index from elastic with error: {e}')
