import json
import boto3

from boto3.dynamodb.conditions import Key
from decimal import Decimal

dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')
table = dynamodb.Table('exercise')

# Decimal encoder is needed because JSON complains about the numbers being
# non-serialisable
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)

def get_exercise_by_type(event):
    # paramters
    exercise_type = event['queryStringParameters']['exercisetype']
    exercise_name = event['queryStringParameters']['exercisename']
    
    response = table.query(
        KeyConditionExpression=Key('type').eq(exercise_type) & Key('name').eq(exercise_name)
    )
    if len(response['Items']) != 0:
        items = response['Items']
    else:
        items = "Not Found"
        
    # response
    responseObject = {}
    responseObject['statusCode'] = 200
    responseObject['headers'] = {}
    responseObject['headers']['Content-Type'] = 'application/json'
    responseObject['body'] = json.dumps(items, cls=DecimalEncoder)
    return responseObject

def get_exercises():
    response = table.scan()
    if len(response['Items']) != 0:
        items = response['Items']
    else:
        items = "Not Found"
        
    # response
    responseObject = {}
    responseObject['statusCode'] = 200
    responseObject['headers'] = {}
    responseObject['headers']['Content-Type'] = 'application/json'
    responseObject['body'] = json.dumps(items, cls=DecimalEncoder)
    return responseObject
    
def get_exercise_by_approval(event):
    approve = event['queryStringParameters']['approval']
    if approve.lower() == 'true':
        approval = True
    else:
        approval = False

    scan_kwargs = {
        'FilterExpression': Key('approved').eq(approval),
        'ProjectionExpression': "#t, #n, approved, description, image_url, #lvl, likes, muscle_groups, upload_date, video_url, #v",
        'ExpressionAttributeNames': {"#t": "type", "#n": "name", "#lvl": "level", "#v": "views"}
    }

    done = False
    start_key = None
    while not done:
        if start_key:
            scan_kwargs['ExclusiveStartKey'] = start_key
        response = table.scan(**scan_kwargs)
        display_exercises = (response.get('Items', []))
        start_key = response.get('LastEvaluatedKey', None)
        done = start_key is None

    if 'Items' in response:
        items = display_exercises
    else:
        items = "Not Found"
        
    # response
    responseObject = {}
    responseObject['statusCode'] = 200
    responseObject['headers'] = {}
    responseObject['headers']['Content-Type'] = 'application/json'
    responseObject['body'] = json.dumps(items, cls=DecimalEncoder)
    return responseObject

def put_exercise_approval(event):
    approve = event['queryStringParameters']['approval']
    exercise_type = event['queryStringParameters']['exercisetype']
    exercise_name = event['queryStringParameters']['exercisename']

    if approve.lower() == 'true':
        approval = True
    else:
        approval = False
        
    table.update_item(
        Key={
            'type': exercise_type,
            'name': exercise_name
        },
        UpdateExpression="set approved=:a",
        ExpressionAttributeValues={
            ':a': approval
        },
        ReturnValues=f"UPDATED_NEW"
    )

    responseObject = {}
    responseObject['statusCode'] = 200
    responseObject['headers'] = {}
    responseObject['headers']['Content-Type'] = 'application/json'
    responseObject['body'] = json.dumps("updated", cls=DecimalEncoder)
    return responseObject

def lambda_handler(event, context):
    if event['httpMethod'] == 'GET':
        if event['queryStringParameters'] is not None:
            if 'exercisetype' in event['queryStringParameters'] and 'exercisename' in event['queryStringParameters']:
                return get_exercise_by_type(event)
            elif 'approval' in event['queryStringParameters']:
                return get_exercise_by_approval(event)
        return get_exercises()
    if event['httpMethod'] == 'PUT':
        return put_exercise_approval(event)
            
