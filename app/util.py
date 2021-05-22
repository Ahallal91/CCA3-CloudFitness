import boto3

def create_table_resource(tablename):
    dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')
    table = dynamodb.Table(tablename)
    return table