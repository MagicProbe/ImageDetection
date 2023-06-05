import boto3
from boto3.dynamodb.conditions import Key

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

bucket_name = 'minipax-image-bucket-fit5225'
table_name = 'images'
table = dynamodb.Table(table_name)
def lambda_handler(event, context):
    url = event['url']
    name = url[url.index('image/'):]

    # Delete the object in S3 with the specified key
    s3.delete_object(Bucket=bucket_name, Key=url[url.index('image/'):])

    # Scan the table to find all items that contain the specified URL
    response = table.query(
        IndexName='name-tag-index',
        KeyConditionExpression=Key('name').eq(name)
    )

    # Delete each item that matches the URL
    with table.batch_writer() as batch:
        for item in response['Items']:
            batch.delete_item(Key={'id': item['id']})

    return {
        'statusCode': 200,
        'body': 'delete successful'
    }
