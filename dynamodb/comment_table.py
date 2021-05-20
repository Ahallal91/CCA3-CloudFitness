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
                    'AttributeName': 'email',
                    'KeyType': 'RANGE'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'id',
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
    except:
        return None
    return table

if __name__ == '__main__':
    comment_table = create_table()
    if comment_table is None:
        print('Table exists')
    else:
        print("Table status:", comment_table.table_status)