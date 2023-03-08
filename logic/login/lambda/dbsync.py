import os
import oracledb
import json
import vault
import oci_sql


def lambda_handler(event, context):
    return_val = {'headers' : {'Content-Type':'application/json'},
                'statusCode': 400,
                'body': 'Login Failed. Invalid user info'
    }

    github_token, vault_addr = os.environ['github_token'], os.environ['vault_addr']

    event_body = json.loads(event['body'])
    user_id = "'" + event_body['sub'] + "'"
    email = "'" + event_body['email'] + "'"

    token = vault.get_token_github(github_token, vault_addr)

    dbdata = vault.get_data(token, vault_addr, 'oci/db')['data']
    un = 'DBUSER'
    pw, cs = dbdata['data'][un], dbdata['data']['ConnectionString']

    query = "SELECT UserId from USER_INFO WHERE UserId = " + user_id

    query_rt = oci_sql.execute_ocidb_sql(query, un, pw, cs, False)
    print(query_rt)

    if len(query_rt) == 0:
        query = """INSERT into USER_INFO (UserId, RegisterDt, UserEmail) 
                VALUES (""" + user_id +  """, SYSDATE, """ + email + """ )"""
        query_rt = oci_sql.execute_ocidb_sql(query, un, pw, cs, True)
        print("New User Updated")
    else: 
        print("User Exists")

    return_val['statusCode'] = 200
    return_val['body'] = "Executed Well"

    return return_val