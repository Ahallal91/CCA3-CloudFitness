import boto3
from boto3.dynamodb.conditions import Key
class Management:
    table = boto3.resource('dynamodb', region_name='ap-southeast-2').Table('exercise')

    def get_exercise_by_approval(self, approval):
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
            response = self.table.scan(**scan_kwargs)
            display_exercises = (response.get('Items', []))
            start_key = response.get('LastEvaluatedKey', None)
            done = start_key is None

        if 'Items' in response:
            return display_exercises
        else:
            return None
    
    def update_exercise_approval(self, type, name, approval):
        response = self.table.update_item(
            Key={
                'type': type,
                'name': name
            },
            UpdateExpression="set approved=:a",
            ExpressionAttributeValues={
                ':a': approval
            },
            ReturnValues=f"UPDATED_NEW"
        )

        return response

    def remove_exercise(self, type, name):
        response = self.table.delete_item(
            Key={
                'type': type,
                'name': name
            })

        return response