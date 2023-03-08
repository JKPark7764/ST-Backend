import json
import boto3
import os

URL = os.environ['websocket_url']
dynamo = boto3.client("dynamodb")
client = boto3.client("apigatewaymanagementapi",  endpoint_url = URL)

def sendToConnectionId(connectionId, payload):
    response = client.post_to_connection(ConnectionId=connectionId, Data=json.dumps(payload))


def getAllConnectionIds():
    global dynamo
    responses = dynamo.scan(TableName="websocket_table")
    connectionIds = [response['Items']['connectionId']['S'] for response in responses]
    return connectionIds

def handler(event, context):
    global client
    
    connectionIds = getAllConnectionIds() if 'target' not in event.keys() else event['target']
    
    # msg = {"message" : "Hello from server!"}
    msg = event['msg']
    
    
    for connection in connectionIds:
        response = client.post_to_connection(ConnectionId=connectionIds, Data=json.dumps(msg))
    
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
