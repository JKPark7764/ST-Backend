import boto3
import json
import os
from botocore.exceptions import ClientError
from boto3.dynamodb.types import TypeDeserializer


ssm = boto3.client('ssm')
parameter = ssm.get_parameter(Name='/lambda/que_name')
que_name = parameter['Parameter']['Value']

dynamodb = boto3.resource('dynamodb')
websocket_table = dynamodb.Table('websocket_table')
client = boto3.client("dynamodb")

sqs = boto3.resource('sqs')
queue = sqs.get_queue_by_name(QueueName=que_name)

deserializer = TypeDeserializer()

def get_live_connection():
    response = websocket_table.scan()
    data = response['Items']

    while 'LastEvaluatedKey' in response:
        response = websocket_table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])
    return data


def get_watch_list(key):
    global client

    try:
        get_result = client.get_item(TableName='watch_list_table',Key=key, ProjectionExpression='watchs')
    except ClientError as err:
        raise err
    else:
        if get_result.get('Item') is None:
            return None
        else:
            deserialised = {k: deserializer.deserialize(v) for k, v in get_result.get("Item").items()}
            response = [{'symbol': x['symbol'], 'market': x['market']} for x in deserialised['watchs']]
            return response
        
def send_messages_to_queue(entries):
    max_batch_size = 10
    chunks = [entries[x:x+max_batch_size] for x in range(0, len(entries), max_batch_size)]

    for chunk in chunks:
        sqs_entries = [{'Id': str(i), 'MessageBody': json.dumps(entry)} for i, entry in enumerate(chunk)]
        response = queue.send_messages(Entries=sqs_entries)

def handler(event, context):
    global dynamodb, queue, websocket_table

    data = get_live_connection()

    if len(data) == 0:
        return {
        'statusCode': 400,
        'headers' : {'Content-Type':'application/json'},
        'body': 'No Active User'
    }

    entries = []

    for user in data:
        print("get watch_list")
        response = get_watch_list({"userId" : {"S": user['userId']}})
        if response is not None : entries.append({"connectionId": user['connectionId'], "data" : response})
    
    send_messages_to_queue(entries)

    return {
        'statusCode': 200,
        'headers' : {
            'Content-Type':'application/json'
        },
        'body': 'Message Sent'
    }
