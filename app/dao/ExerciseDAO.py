import boto3
from decimal import Decimal
from datetime import datetime

from boto3.dynamodb.conditions import Key, Attr, Or

from functools import reduce

class ExerciseDAO:
    dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')
    table = dynamodb.Table('exercise')

    def format_tags(tags):
        return tags.split(',')


    def upload_exercise(self, partition_exercise_type, formatted_exercise_type, sort_name, formatted_name, search,
                        level, muscle_groups, description, video_url, image_url, admin_approved):
        response = self.table.put_item(
            Item={
                'type': partition_exercise_type,  # type of exercise, e.g. compound, body-weight, etc.
                'formatted_type': formatted_exercise_type,  # original type as selected, e.g. "Compound", "Body weight"
                'name': sort_name,  # stripped name used as sort key, e.g. "romanian-deadlift"
                'formatted_name': formatted_name,  # original name user entered, e.g. "Romanian deadlift"
                'search': search,  # duplicate of name to enable searching of attributes
                'level': level,  # difficulty level, e.g. beginner, intermediate, etc.
                'muscle_groups': muscle_groups,  # list of muscle groups, e.g. neck, triceps, biceps, etc.
                'description': description,  # user-given description of that exercise
                'video_url': video_url,  # video url
                'image_url': image_url,
                'approved': admin_approved,  # true if an admin has approved the workout, false otherwise
                'upload_date': str(datetime.now()),  # upload date in the format YYYY-MM-DD HH:MM:SS.MS
                'views': 0,  # number of times exercise has been viewed by all users
                'likes': 0,  # number of likes exercise has received from registered users
            }
        )

        return response


    def update_exercise(self, exercise_type, name, views=None, likes=None):
        increment = 1

        if views is not None:
            expression = "SET #a = #a + :val"
            attribute = "views"
        if likes is not None:
            expression = "SET #a = #a + :val"
            attribute = "likes"
        response = self.table.update_item(
            Key={
                'type': exercise_type,
                'name': name
            },
            UpdateExpression=expression,
            ExpressionAttributeValues={
                ':val':Decimal(increment)
            },
            ExpressionAttributeNames={
                "#a": attribute
            },
            ReturnValues=f"UPDATED_NEW"
        )

        return response


    def get_exercise(self, exercise_type, name):
        response = self.table.query(
            KeyConditionExpression=Key('type').eq(exercise_type) & Key('name').eq(name)
        )

        return response['Items']


    def search_by_query(self, query):
        split_query = query.split(' ')
        response = self.table.scan(
            FilterExpression=reduce(Or, [(Attr("search").contains(value)) for value in split_query]))
        return response["Items"]