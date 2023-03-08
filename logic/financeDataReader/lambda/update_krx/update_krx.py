import json
import FinanceDataReader as fdr
import pandas as pd
import numpy as np
import oci_sql
import vault
import os

def handler(event, context):
    github_token, vault_addr = os.environ['github_token'], os.environ['vault_addr']

    # Oracle DB setup
    token = vault.get_token_github(github_token, vault_addr)
    dbdata = vault.get_data(token, vault_addr, 'oci/db')['data']
    un = 'DBUSER'
    pw, cs = dbdata['data'][un], dbdata['data']['ConnectionString']

    # # Delete all data in STOCK_TODAY
    query = """DELETE from STOCK_TODAY"""
    oci_sql.execute_ocidb_sql(query, un, pw, cs, True)


    # Insert FinanceReader data
    target_col = ["ISU_CD", "Name","Market","Close","Changes",
                "ChagesRatio","Open","High","Low","Volume","Amount"]
    df_krx = fdr.StockListing("KRX")[target_col]


    list_krx = df_krx.values.tolist()
    query = """INSERT INTO STOCK_TODAY
            (ISU_CD,Name,Market,Close,Changes,ChagesRatio,Open,High,Low,Volume,Amount)
            VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11)"""
    query_return = oci_sql.excutemany_ocidb_sql(query, list_krx, un, pw, cs, True)

    return {
        'statusCode': 200,
        'body': json.dumps('All executed!')
    }

