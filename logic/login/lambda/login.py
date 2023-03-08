import os
import json
import oracledb

def execute_ocidb_sql(query, un, pw, cs):
    with oracledb.connect(user=un, password=pw, dsn=cs) as connection:
        with connection.cursor() as cursor:
            sql = query
            func_return = []
            query_return = cursor.execute(sql)
            if query_return != None: 
                for r in query_return:
                    func_return.append(r[0])
                return func_return


def lambda_handler(event, context):
    return_val = {'headers' : {'Content-Type':'application/json'},
                'statusCode': 400,
                'body': 'Login Failed. Invalid user info'
    }

    event_body = json.loads(event['body'])
    un, pw, cs = os.environ['un'], os.environ['pw'], os.environ['cs']
    id = event_body['id']
    passwd = event_body['passwd']

    query = "SELECT password from USER_INFO WHERE UserId = '" + id + "'"

    #ID check
    if ' ' in id : return return_val


    query_rt = execute_ocidb_sql(query, un, pw, cs)
    print(query_rt)

    
    if passwd == query_rt[0]:
        return_val['statusCode'] = 200
        return_val['body'] = 'Login Success'
    else:
        return_val['statusCode'] = 400
        return_val['body'] = 'Login Failed. Incorrect user info'
    
    return return_val
