import os
import vault
import json
import FinanceDataReader as fdr
import pandas as pd
import numpy as np
import oci_sql

def handler(event, context):
    github_token, vault_addr = os.environ['github_token'], os.environ['vault_addr']

    # # Oracle DB setup
    token = vault.get_token_github(github_token, vault_addr)
    dbdata = vault.get_data(token, vault_addr, 'oci/db')['data']
    un = 'DBUSER'
    pw, cs = dbdata['data'][un], dbdata['data']['ConnectionString']
    query = """DELETE from STOCK_LIST"""
    oci_sql.execute_ocidb_sql(query, un, pw, cs, True)

    
    df = pd.DataFrame()
    target_col = ["Code", "Name", "Market"]
    stocks = fdr.StockListing('KRX')[target_col]
    stocks.rename(columns = {'Code' : 'Symbol'}, inplace=True)
    df = pd.concat([df, stocks])
    
    target_col = ["Symbol", "Name",]
    for market in ['NYSE', 'NASDAQ', 'AMEX', 'S&P500']:
        print('Market loading : ' + market)
        stocks = fdr.StockListing(market)[target_col]
        stocks["Market"] = market
        df = pd.concat([df, stocks])
        print('Market loaded : ' + market)
    
    print(df.shape)
    print(df.describe())
    df['Origin'] = 'fdr'
    data = df.values.tolist()
    
    query = """INSERT INTO STOCK_LIST
            (Symbol,Name,Market,Origin)
            VALUES (:1, :2, :3, :4)"""
    oci_sql.excutemany_ocidb_sql(query, data , un, pw, cs, True)

    return {
        'statusCode': 200,
        'body': json.dumps('All executed!')
    }