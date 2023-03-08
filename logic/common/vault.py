import requests
import json

def get_token_github(github_token, vault_addr):
    #Get token with github
    VAULT_ADDR = vault_addr
    vault_return = requests.post('https://' + VAULT_ADDR  + ':8200/v1/auth/github/login',
            data={"token": github_token}, timeout=10)
        
    if vault_return.status_code == 200:
        json_return = json.loads(vault_return.text)
        return json_return['auth']['client_token']
    else: 
        raise Exception('Github login error' + ' status_code: ' + str(vault_return.status_code) + 'reason : ' + vault_return.reason)



def get_data(token, vault_addr, kv_data_path):
    vault_return = requests.get('https://' + vault_addr + ':8200/v1/kv/data/' + kv_data_path,
            headers={'X-Vault-Token': token}, timeout=10)

    if vault_return.status_code == 200:
        return json.loads(vault_return.text)
    else:
        raise Exception('Vault get data error' + ' status_code: ' + str(vault_return.status_code) + 'reason : ' + vault_return.reason)