import boto3
import json

dynamodb = boto3.resource('dynamodb')

table_name = 'images'

def lambda_handler(event, context):
    table = dynamodb.Table(table_name)
    tags = event['tags']
    for obj in tags:
        tag = obj['tag']
        count = obj['count']

        response = table.scan(FilterExpression='contains(#tags, :val)',
                          ExpressionAttributeNames={'#tags': 'tags'},
                          ExpressionAttributeValues={':val': tag})

        ans = []
        for item in response['Items']:
            ans.append()


    return {
        'statusCode': 200,
        'body': 'delete successful'
    }
