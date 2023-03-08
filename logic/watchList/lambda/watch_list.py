import boto3
import json
from botocore.exceptions import ClientError
from boto3.dynamodb.types import TypeDeserializer
from boto3.dynamodb.types import TypeSerializer


client = boto3.client("dynamodb")
deserializer = TypeDeserializer()
serializer = TypeSerializer()


def get_item(table_name, key):
    global client

    try:
        get_result = client.get_item(
            TableName=table_name,
            Key=key
        )
    except ClientError as err:
        raise err
    else:
        if get_result.get('Item') is None:
            return None
        else:
            deserialised = {k: deserializer.deserialize(v) for k, v in get_result.get("Item").items()}
            return deserialised

def put_item(table_name, item):
    try:
        print({k: serializer.serialize(v) for k,v in item.items()})
        response = client.put_item(
            TableName=table_name,
            Item = {k: serializer.serialize(v) for k,v in item.items()}
        )
    except ClientError as err:
        raise err
    else:
        return response

def handler(event, context):
    global client
    
    event_body = json.loads(event['body'])
    user_id = event_body['sub']
    mode = event_body['mode']
    
    if mode == 'get':
        response = get_item("watch_list_table", {"userId" : {"S": user_id}})
        print(response)

    elif mode == 'update':
        item = event_body['item']
        print(item)
        put_item("watch_list_table", {
            "userId": user_id,
            "watchs": item}
        )
        response = "Updated successfully"
    
    return {
        'statusCode': 200,
        'headers' : {
            'Content-Type':'application/json'
        },
        'body': json.dumps(response)
    }
