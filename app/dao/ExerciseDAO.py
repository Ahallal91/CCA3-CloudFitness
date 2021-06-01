import boto3
from datetime import datetime

from boto3.dynamodb.conditions import Key


def format_tags(tags):
    return tags.split(',')


def upload_exercise(name, exercise_type, level, muscle_groups, description, video_url, image_url, admin_approved):
    dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')
    table = dynamodb.Table('exercise')
    response = table.put_item(
        Item={
            'name': name,  # name of the exercise, e.g. "squat"
            'type': exercise_type,  # type of exercise, e.g. compound, body weight, etc
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


def get_exercise(exercise_type, name, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')

    table = dynamodb.Table('exercise')

    response = table.query(
        KeyConditionExpression=Key('type').eq(exercise_type) & Key('name').eq(name)
    )

    return response['Items']