import oracledb
import requests
import json

def execute_ocidb_sql(query, un, pw, cs, commit_yn):
    with oracledb.connect(user=un, password=pw, dsn=cs) as connection:
        with connection.cursor() as cursor:
            sql = query
            func_return = []
            query_return = cursor.execute(sql)
            if commit_yn :
                cursor.execute("commit")
            if query_return != None: 
                for r in query_return:
                    func_return.append(r)
                    print(r)
                return func_return

def excutemany_ocidb_sql(query, data, un, pw, cs, commit_yn):
    with oracledb.connect(user=un, password=pw, dsn=cs) as connection:
        with connection.cursor() as cursor:
            sql = query
            func_return = []
            query_return = cursor.executemany(sql, data)
            if commit_yn :
                cursor.execute("commit")
            if query_return != None: 
                for r in query_return:
                    func_return.append(r)
                    print(r)
                return func_return
