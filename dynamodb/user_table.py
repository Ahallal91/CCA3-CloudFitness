import boto3

def create_user_table():
    dynamodb = boto3.resource('dynamodb')
    try:
        table = dynamodb.create_table(
            TableName='user',
            KeySchema=[
                {
                    'AttributeName': 'email',
                    'KeyType': 'HASH'  
                }
            ],
            AttributeDefinitions=[
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
    except:
        return None
    return table

if __name__ == '__main__':
    user_table = create_user_table()
    if user_table is None:
        print('Table exists')
    else:
        print("Table status:", user_table.table_status)