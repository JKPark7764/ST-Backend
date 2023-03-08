import json
import boto3
import FinanceDataReader as fdr
import os

ssm = boto3.client('ssm')
parameter = ssm.get_parameter(Name='/lambda/exchange_date')
date_ref = json.loads(parameter['Parameter']['Value'])
parameter = ssm.get_parameter(Name='/lambda/websocket_url')
URL = parameter['Parameter']['Value']

client = boto3.client("apigatewaymanagementapi",  endpoint_url = URL, region_name = 'us-west-2')

def send_to_connectionId(connectionId, payload):
    global client
    response = client.post_to_connection(ConnectionId=connectionId, Data=json.dumps(payload))

def get_live_price(stocks):
    global date_ref
    dict = {}

    for stock in stocks:
        try:
            response = fdr.DataReader(stock['symbol'], date_ref[stock['market']], date_ref[stock['market']])
        except:
            print("Error while getting stock price. Ticker/Market : " + stock['symbol'] + date_ref[stock['market']])
            continue
        if response.empty : continue
        else: response.reset_index(drop=True, inplace=True)

        if stock['market'] in ['KOSPI', 'KONEX', 'KOSDAQ GLOBAL', 'KOSDAQ']:
            response['Change'] = response['Change'].round(4) * 100
            response['Close'] = response.apply(lambda x: str(x['Close']) + '\\', axis=1)
        else :
            response['Change'] = response.apply(lambda x: (x['Close'] / x['Open']).round(4) * 100, axis=1)
            response['Close'] = response.apply(lambda x: str(x['Close'].round(3)) + '$', axis=1)
                  

        dict[stock['symbol']] = response.to_dict('r')[0]
    
    return dict

def handler(event, context):
           
    for message in event['Records']:
        body = json.loads(message['body'])
        connectionId = body['connectionId']
        
        response = get_live_price(body['data'])
        payload = {'type' : 'live'}
        payload['data'] = response
        send_to_connectionId(connectionId, payload)

    return {
        'statusCode': 200,
        'body': json.dumps('Live price message sent')
    }
