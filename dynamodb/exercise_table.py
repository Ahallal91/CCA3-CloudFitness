import boto3
from botocore.exceptions import ClientError


def create_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource("dynamodb", region_name="ap-southeast-2")

    table_name = 'exercise'

    dynamodb = boto3.resource('dynamodb')
    try:
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'body_part',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'name',
                    'KeyType': 'RANGE'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'id',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'title',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceInUseException':
            print(f"Table {table_name} already exists")
        elif e.response['Error']['Code'] == 'InternalServerError':
            print("An unknown error occured on the server side. HTTP Status Code: 500")
        return None

    table.wait_until_exists()
    return table


if __name__ == '__main__':
    exercise_table = create_table()
    if exercise_table is None:
        print('Table exists')
    else:
        print("Table status:", exercise_table.table_status)
