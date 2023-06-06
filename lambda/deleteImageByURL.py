import json
import boto3
from boto3.dynamodb.conditions import Key

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

bucket_name = 'minipax-image-bucket-fit5225'
table_name = 'images'
table = dynamodb.Table(table_name)


def lambda_handler(event, context):
    body = json.loads(event['body'])
    url = body['url']
    key = url.replace("https://minipax-image-bucket-fit5225.s3.amazonaws.com/", "")

    username = event['requestContext']['authorizer']['claims']['cognito:username']

    param_username = url.replace("https://minipax-image-bucket-fit5225.s3.amazonaws.com/", "").split("/")[0]
    if username != param_username:
        return {
            'statusCode': 400,
            'body': json.dumps('Unauthorized!')
        }

    # Delete the object in S3 with the specified key
    s3.delete_object(Bucket=bucket_name, Key=key)

    # Scan the table to find all items that contain the specified URL
    response = table.query(
        IndexName='S3URL-tag-index',
        KeyConditionExpression=Key('S3URL').eq(url)
    )

    # Delete each item that matches the URL
    with table.batch_writer() as batch:
        for item in response['Items']:
            batch.delete_item(Key={'id': item['id']})

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*'
        },
        'body': 'delete successful'
    }
