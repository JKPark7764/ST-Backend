from yahoo_fin.stock_info import get_data
import pandas as pd
import json

def handler(event, context):
    event_body = json.loads(event['body'])
    start_date = event_body['start_date']
    end_date = event_body['end_date']
    tickers = event_body['tickers']
    interval = event_body['interval']

    df = pd.DataFrame()

    try:
        for ticker in tickers:
            data = get_data(ticker, start_date=start_date, end_date=end_date, index_as_date = False, interval=interval)
            df = pd.concat([df, data])
    except:
        print('Failed while getting data of ' + ticker)

    df.reset_index(drop=True, inplace=True)
    df['json'] = df.apply(lambda x: x.to_json(), axis=1)

    return {
    'statusCode': 200,
    'headers' : {
        'Content-Type':'application/json'
    },
        'body': df['json'].to_json()
    }
