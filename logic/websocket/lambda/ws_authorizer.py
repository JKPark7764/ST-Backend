import json
import jwt
import os
import vault

github_token, vault_addr = os.environ['github_token'], os.environ['vault_addr']
token = vault.get_token_github(github_token, vault_addr)
auth0data = vault.get_data(token, vault_addr, 'Auth0/key')['data']
public_key = auth0data['data']['public_key']
audience = auth0data['data']['audience']


def lambda_handler(event, context):
    global public_key, audience
    print(event['queryStringParameters'])

    # Extract the JWT token from the request context
    jwt_token = event['queryStringParameters']['jwtToken']
    
    # Decode the JWT token
    try:
        decoded_jwt = jwt.decode(jwt_token, public_key, audience=audience, algorithms=["RS256"])
    except jwt.InvalidSignatureError as e:
        print(e)
        return {
            "statusCode": 401,
            "body": json.dumps({
                "error": "Unauthorized"
            })
        }

    # Build the policy document
    policy = {
        "principalId": decoded_jwt['sub'],
        "policyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "execute-api:Invoke",
                    "Effect": "Allow",
                    "Resource": event['methodArn']
                }
            ]
        }
    }

    return policy
