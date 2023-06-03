import boto3
import json

dynamodb = boto3.resource('dynamodb')

table_name = 'images'


def lambda_handler(event, context):
    table = dynamodb.Table(table_name)
    for obj in event['tags']:
        tag = obj['tag']
        count = obj['count']



        response = table.scan(FilterExpression='contains(#tag, :val)',
                          ExpressionAttributeNames={'#tag': 'tag'},
                          ExpressionAttributeValues={':val': tag})

        for item in response['Items']:


    return {
        'statusCode': 200,
        'body': 'delete successful'
    }
