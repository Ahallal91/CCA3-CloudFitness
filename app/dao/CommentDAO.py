import boto3
from datetime import datetime

from boto3.dynamodb.conditions import Key

class CommentDAO:
    table = boto3.resource('dynamodb', region_name='ap-southeast-2').Table('comments')

    def create_comment(self, exercise_type, email, comment):
        response = self.table.put_item(
            Item={
                'type': exercise_type,
                'email': email,
                'comments': [
                    {
                        'timestamp': str(datetime.now()),
                        'comment': comment
                    }
                ]
            }
        )

        return response

    def update_comment(self, exercise_type, email, comment):
        response = self.table.update_item(
            Key={
                'type': exercise_type,
                'email': email
            },
            UpdateExpression="SET comments = list_append(comments, :c)",
            ExpressionAttributeValues={
                ':c': [{'timestamp': str(datetime.now()),
                        'comment' : comment}]
            },
            ReturnValues=f"UPDATED_NEW"
        )

        return response
    
    def upload_comment(self, exercise_type, email, comment):
        # check if the user already made a comment on that exercise
        exercise_type = str(exercise_type)
        email = str(email)

        response = self.table.query(
            KeyConditionExpression=Key('type').eq(exercise_type) & Key('email').eq(email)
        )
        print(response)
        if 'Items' in response and len(response['Items']) != 0:
            self.update_comment(exercise_type, email, comment)
        else:
            self.create_comment(exercise_type, email, comment)

    def get_comments(self, exercise_type, email=None):
        if email is None:
            response = self.table.query(
                KeyConditionExpression=Key('type').eq(exercise_type)
            )
        else:
            response = self.table.query(
                KeyConditionExpression=Key('type').eq(exercise_type) & Key('email').eq(email)
            )

        return response['Items']