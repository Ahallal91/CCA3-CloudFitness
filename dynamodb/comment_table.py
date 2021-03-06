import boto3
from botocore.exceptions import ClientError

def create_table():
    dynamodb = boto3.resource("dynamodb", region_name="ap-southeast-2")
    try:
        table_name = 'comments'
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'type',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'email',
                    'KeyType': 'RANGE'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'type',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'email',
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
    comment_table = create_table()
    if comment_table is None:
        print('Table exists')
    else:
        print("Table status:", comment_table.table_status)