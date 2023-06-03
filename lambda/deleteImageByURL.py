import boto3

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

bucket_name = 'minipax-image-bucket-fit5225'
table_name = 'images'

def lambda_handler(event, context):
    url = event['url']

    # Delete the object in S3 with the specified key
    s3.delete_object(Bucket=bucket_name, Key=url[url.index('image/'):])

    # Scan the table to find all items that contain the specified URL
    table = dynamodb.Table(table_name)
    response = table.scan(FilterExpression='contains(#S3URL, :val)',
                          ExpressionAttributeNames={'#S3URL': 'S3URL'},
                          ExpressionAttributeValues={':val': url})

    # Delete each item that matches the URL
    with table.batch_writer() as batch:
        for item in response['Items']:
            batch.delete_item(Key={'id': item['id']})

    return {
        'statusCode': 200,
        'body': 'delete successful'
    }
