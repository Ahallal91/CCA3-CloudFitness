import boto3
from datetime import datetime

from boto3.dynamodb.conditions import Key

class ProfilePersonalDAO:
    table = boto3.resource('dynamodb', region_name='ap-southeast-2').Table('profile-personal')

    def add_exercise(self, partition_exercise_type, formatted_exercise_type, sort_name, formatted_name, search,
                        level, muscle_groups, description, video_url, image_url, email):
                        
        response = self.table.put_item(
            Item={
                'email': email, # user email
                'exercise': partition_exercise_type + sort_name,  # type of exercise, e.g. compound, body-weight, etc.
                'type': partition_exercise_type,
                'formatted_type': formatted_exercise_type,  # original type as selected, e.g. "Compound", "Body weight"
                'name': sort_name,  # stripped name used as sort key, e.g. "romanian-deadlift"
                'formatted_name': formatted_name,  # original name user entered, e.g. "Romanian deadlift"
                'search': search,  # duplicate of name to enable searching of attributes
                'level': level,  # difficulty level, e.g. beginner, intermediate, etc.
                'muscle_groups': muscle_groups,  # list of muscle groups, e.g. neck, triceps, biceps, etc.
                'description': description,  # user-given description of that exercise
                'video_url': video_url,  # video url
                'image_url': image_url,
                'upload_date': str(datetime.now()),  # upload date in the format YYYY-MM-DD HH:MM:SS.MS
                'personal': True
            }
        )

        return response

    def remove_exercise(self, type, name, email):
        response = self.table.delete_item(
            Key={
                'email': email,
                'exercise': type+name

            })

        return response

    def get_exercises(self, email):
        response = self.table.query(
            KeyConditionExpression=Key('email').eq(email)
        )

        return response['Items']
    
    def get_exercise(self, type, name, email):
        response = self.table.query(
            KeyConditionExpression=Key('email').eq(email) & Key('exercise').eq(type+name)
        )

        return response['Items']