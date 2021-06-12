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


def get_exercises_by_approval(approval):
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

    return json.dumps(items, indent=2, cls=DecimalEncoder)


def get_approved_exercises(path_parameters):
    return get_exercises_by_approval(True)
    

def get_pending_exercises(path_parameters):
    return get_exercises_by_approval(False)


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
    responseObject['body'] = json.dumps("updated", indent=2, cls=DecimalEncoder)
    return responseObject


def root(path_parameters):
    return json.dumps("root", indent=2, cls=DecimalEncoder)


def get_all_exercises(path_parameters):
    table = dynamodb.Table("exercise")
    response = table.scan()
    if len(response['Items']) != 0:
        items = response['Items']
    else:
        items = "Not Found"
    return json.dumps(items, indent=2, cls=DecimalEncoder)
    

def get_all_exercise_types(path_parameters):
    table = dynamodb.Table("metadata")
    response = table.query(
        KeyConditionExpression=Key("name").eq("exercise_types")
    )
    result = response["Items"][0]
    return json.dumps(result, indent=2, cls=DecimalEncoder)


def get_exercises_by_type(path_parameters):
    table = dynamodb.Table('exercise')
    response = table.query(
        KeyConditionExpression=Key("type").eq(path_parameters["type"])
    )
    if len(response['Items']) != 0:
        response = response['Items']
    else:
        response = "No exercise type named '" + path_parameters["type"] + "' was found."
    return json.dumps(response, indent=2, cls=DecimalEncoder)


def get_exercise_by_type_and_name(path_parameters):
    table = dynamodb.Table('exercise')

    response = table.query(
        KeyConditionExpression=Key('type').eq(path_parameters["type"]) & Key('name').eq(path_parameters["name"])
    )
    if len(response['Items']) != 0:
        response = response['Items'][0]
    else:
        response =  "No exercise with type '" + path_parameters["type"] + "' and name '" + path_parameters["name"] + "' was found."
    return json.dumps(response, indent=2, cls=DecimalEncoder)


def lambda_handler(event, context):
    responseObject = {}
    responseObject['statusCode'] = 200
    responseObject['headers'] = {}
    responseObject['headers']['Content-Type'] = 'application/json'
    # responseObject['body'] = json.dumps(event, indent=2, cls=DecimalEncoder)
    # return responseObject
    
    resources = {
            "/" : root,
            "/exercises" : get_all_exercises,
            "/exercises/types" : get_all_exercise_types,
            "/exercises/{type}" : get_exercises_by_type,
            "/exercises/{type}/{name}" : get_exercise_by_type_and_name,
            "/exercises/approved" : get_approved_exercises,
            "/exercises/pending" : get_pending_exercises
    }
    
    path_parameters = event["pathParameters"]

    if event['httpMethod'] == 'GET':
        responseObject['body'] = resources[event["resource"]](path_parameters)
        return responseObject
        
    if event['httpMethod'] == 'PUT':
        return put_exercise_approval(event)
            
