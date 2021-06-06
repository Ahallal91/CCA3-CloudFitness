import boto3
from datetime import datetime

from boto3.dynamodb.conditions import Key

class ProfileExistingDAO:
    table = boto3.resource('dynamodb', region_name='ap-southeast-2').Table('profile-existing')
    def add_existing_exercise(self, type, name, email):

        response = self.table.put_item(
        Item={
            'email': email, 
            'exercise': type+name, 
            'exercise-type': type,
            'exercise-name': name
        }
    )

        return response

    def remove_existing_exercise(self, type, name, email):
        response = self.table.delete_item(
            Key={
                'email': email,
                'exercise': type+name
            })

        return response

    def get_existing_exercises(self, email):
        response = self.table.query(
            KeyConditionExpression=Key('email').eq(email)
        )

        return response['Items']