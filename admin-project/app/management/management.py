import boto3
from functools import reduce
from boto3.dynamodb.conditions import Key, And

class Management:
    def get_exercise_by_approval(approval):
        dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')
        table = dynamodb.Table('exercise')
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
            return display_exercises
        else:
            return None
    
    def update_exercise_approval(type, name, approval):
        dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')
        table = dynamodb.Table('exercise')
        response = table.update_item(
            Key={
                'type': type,
                'name': name
            },
            UpdateExpression="set approved=:a",
            ExpressionAttributeValues={
                ':a': approval
            },
            ReturnValues=f"UPDATED_APPROVAL: {approval}"
        )

        return response