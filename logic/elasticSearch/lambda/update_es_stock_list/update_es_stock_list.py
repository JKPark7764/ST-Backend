import os
import vault
import oci_sql
from elasticsearch import Elasticsearch, helpers

def handler(event, context):
    github_token, vault_addr = os.environ['github_token'], os.environ['vault_addr']

    # Oracle DB setup
    token = vault.get_token_github(github_token, vault_addr)
    dbdata = vault.get_data(token, vault_addr, 'oci/db')['data']
    un = 'DBUSER'
    pw, cs = dbdata['data'][un], dbdata['data']['ConnectionString']
    
    # ES setup
    esdata = vault.get_data(token, vault_addr, 'ES/info')['data']
    es_addr = esdata['data']['internal_addr']
    esdata = vault.get_data(token, vault_addr, 'ES/user')['data']
    es_pw = esdata['data']['elastic']

    # Get STOCK_LIST from Oracle DB
    query = """SELECT symbol, name, market from STOCK_LIST"""
    response = oci_sql.execute_ocidb_sql(query, un, pw, cs, False)

    # Update ES
    docs = [{"_index" : "stock_list", 
            "_source" : {"symbol" : stock[0], "name" : stock[1], "market": stock[2]}} for stock in response]

    crt_path = os.environ['LAMBDA_TASK_ROOT'] + "/http_ca.crt"
    es = Elasticsearch('https://elastic:' + es_pw + '@' + es_addr + ':9200',
                        ca_certs=crt_path)
        
    response = helpers.bulk(es, docs)
    
    print(response)
    
    return {
        'statusCode': 200,
        'headers' : {
            'Content-Type':'application/json'
        },
        'body': 'Good'
    }
