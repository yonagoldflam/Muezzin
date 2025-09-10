from fastapi import FastAPI
from utils.elastic_search.elastic_dal import ElasticDal

app = FastAPI()
elastic_client = ElasticDal()

index_name = 'muezzin_podcasts'

@app.get("/BDS_supporters")
def get_all_soldiers():
    query = {
        'query': {
            'match': {
                'is_bds': True
            }
        }
    }
    bds_supporters_list = elastic_client.search(index=index_name, query=query)
    return bds_supporters_list

@app.get("/all_podcasts")
def get_all_soldiers():
    query = {
        'query': {
            'match_all': {}
        }
    }
    bds_supporters_list = elastic_client.search(index=index_name, query=query)
    return bds_supporters_list
