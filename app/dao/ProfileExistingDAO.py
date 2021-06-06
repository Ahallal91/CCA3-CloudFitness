import boto3
from datetime import datetime

from boto3.dynamodb.conditions import Key

class ProfileExistingDAO:
    table = boto3.resource('dynamodb', region_name='ap-southeast-2').Table('profile-existing')
    def add_existing_exercise(self, type, name, email):

        response = self.table.put_item(
        Item={
            'exercise': type+name, 
            'email': email, 
            'exercise-type': type,
            'exercise-name': name
        }
    )

        return response

    def remove_existing_exercise(self, type, name, email):
        response = self.table.delete_item(
            Key={
                'exercise': type+name, 
                'email': email 
            })

        return response