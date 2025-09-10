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
    podcasts_list = elastic_client.search(index=index_name, query=query)
    return podcasts_list

@app.get("/high")
def get_all_high():
    query = {
        'query': {
            'match': {
                'bds_threat_level': 'high'
            }
        }
    }
    bds_list = elastic_client.search(index=index_name, query=query)
    return bds_list

@app.get("/medium")
def get_all_high():
    query = {
        'query': {
            'match': {
                'bds_threat_level': 'medium'
            }
        }
    }
    bds_list = elastic_client.search(index=index_name, query=query)
    return bds_list

@app.get("/none")
def get_all_high():
    query = {
        'query': {
            'match': {
                'bds_threat_level': 'none'
            }
        }
    }
    bds_list = elastic_client.search(index=index_name, query=query)
    return bds_list