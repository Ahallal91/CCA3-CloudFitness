import boto3

def create_table():
    dynamodb = boto3.resource('dynamodb')
    try:
        table = dynamodb.create_table(
            TableName='comments',
            KeySchema=[
                {
                    'AttributeName': 'id',
                    'KeyType': 'HASH'  
                },
                {
                    'AttributeName': 'title',
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
    except:
        return None
    return table

if __name__ == '__main__':
    exercise_table = create_table()
    if exercise_table is None:
        print('Table exists')
    else:
        print("Table status:", exercise_table.table_status)