import boto3
import json

s3 = boto3.client('s3')


def lambda_handler(event, context):
    body = json.loads(event['body'])
    image_name = body['name']
    image_value = body['value']

    username = event['requestContext']['authorizer']['claims']['cognito:username']

    bucket_name = 'minipax-image-bucket-fit5225'
    object_key = username + '/image/' + image_name
    object_data = image_value

    # Check if the object already exists
    try:
        s3.head_object(Bucket=bucket_name, Key=object_key)
        return {
            'statusCode': 400,
            'body': f'{object_key} already exists in {bucket_name}'
        }
    except Exception as e:
        # If the exception is ClientError and error code is 404, means the object does not exist
        if e.__class__.__name__ == 'ClientError' and e.response['Error']['Code'] == '404':
            pass
        else:
            raise e

    # Write the object to S3
    s3.put_object(Bucket=bucket_name, Key=object_key, Body=object_data)

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*'
        },
        'body': 'upload image successful'
    }