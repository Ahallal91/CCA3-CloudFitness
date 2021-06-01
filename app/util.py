import boto3


def create_table_resource(tablename):
    dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')
    table = dynamodb.Table(tablename)
    return table


def get_exercise_levels():
    return ["Beginner", "Intermediate", "Advanced", "Expert"]


def get_muscle_groups():
    return ["Neck",
            "Traps",
            "Shoulders",
            "Chest",
            "Triceps",
            "Biceps",
            "Forearms",
            "Abdominals",
            "Middle back",
            "Lats",
            "Lower back",
            "Glutes",
            "Quadriceps",
            "Hamstrings",
            "Calves"]


def get_exercise_types():
    return ["Compound",
            "Free weight",
            "Machine",
            "Bodyweight",
            "Cardio"]
