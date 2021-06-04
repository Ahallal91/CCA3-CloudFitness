# THIS WAS HERE BY DEFAULT
# import json

# def lambda_handler(event, context):
#     # TODO implement
#     return {
#         'statusCode': 200,
#         'body': json.dumps('Hello from Lambda!')
#     }

import json
import boto3

from decimal import Decimal

dynamodb = boto3.resource('dynamodb')

# Decimal encoder is needed because JSON complains about the numbers being
# non-serialisable
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)

def lambda_handler(event, context):
    table = dynamodb.Table('exercise')
    body = table.scan()
    items = body['Items']
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            'Access-Control-Allow-Credentials': 'true',
            'Content-Type': 'application/json'
        },
        'body': json.dumps(items, cls=DecimalEncoder)
    }