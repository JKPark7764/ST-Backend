import json
import boto3
import jwt

return_msg = {
    "on_connect": "Connected",
    "on_disconnect": "Disconnected",
    "default": "Default route invoked!"
}


def lambda_handler(event, context):
    # TODO implement
    route = event["requestContext"].get('routeKey')
    msg = return_msg['default']

    if route in ['$disconnect', '$connect']:
        client = boto3.client("dynamodb")
        if route == '$disconnect':
            client.delete_item(TableName="websocket_table", Key = {"connectionId" : {"S": event["requestContext"].get("connectionId")}})
            msg = return_msg['on_disconnect']
        else:
            # Decode the JWT token
            jwt_token = event['queryStringParameters']['jwtToken']
            decoded_jwt = jwt.decode(jwt_token, options={"verify_signature": False})

            client.put_item(TableName="websocket_table", 
            Item={"connectionId" : {"S": event["requestContext"].get("connectionId")},
                  "userId" : {"S": decoded_jwt['sub']}})
            msg = return_msg['on_connect']   

    return {
        'statusCode': 200,
        'body': json.dumps(msg)
    }

    
