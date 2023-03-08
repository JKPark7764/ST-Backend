import os
import vault
import json
from elasticsearch import Elasticsearch, helpers

es_addr = None
es_pw = None
es = None

def make_query(word):
    query = {"query": {
                "bool": {
                    "should": [
                        {
                            "match_phrase_prefix": {
                                "symbol": {
                                    "query": "{}*".format(word)
                                }
                            }
                        },
                        {
                            "match_phrase_prefix": {
                                "market": {
                                    "query": "{}*".format(word)
                                }
                            }
                        },
                        {
                            "match_phrase_prefix": {
                                "name": {
                                    "query": "{}*".format(word)
                                }
                            }
                        }
                    ],
                    "filter": [],
                    "must": [],
                    "must_not": []
                }
            }
        }
    return query

def fetch_vault(renew_yn):
    global es_addr, es_pw, es

    if not es_addr or not es_pw or not es or renew_yn == True:
        github_token, vault_addr = os.environ['github_token'], os.environ['vault_addr']
        token = vault.get_token_github(github_token, vault_addr)
        
        # ES setup
        esdata = vault.get_data(token, vault_addr, 'ES/info')['data']
        es_addr = esdata['data']['internal_addr']
        esdata = vault.get_data(token, vault_addr, 'ES/user')['data']
        es_pw = esdata['data']['elastic']

        crt_path = os.environ['LAMBDA_TASK_ROOT'] + "/http_ca.crt"
        es = Elasticsearch('https://elastic:' + es_pw + '@' + es_addr + ':9200',
                ca_certs=crt_path)

def handler(event, context):
    global es
    event_body = json.loads(event['body'])
    renew_yn = event_body['renew_yn']
    word = event_body['word']

    fetch_vault(renew_yn)
    
    status_code = 200

    try:
        query = make_query(word)
        data = es.search(index='stock_list', body=query)
        hits = data['hits']['hits']
        response = {}
        response['data'] = [x['_source'] for x in hits]
        response['type'] = 'search'
    except:
        response = 'Failed getting data from ES'
        status_code = 400

    
    return {
        'statusCode': status_code,
        'headers' : {
            'Content-Type':'application/json'
        },
        'body': json.dumps(response, default=str, ensure_ascii=False)
    }
