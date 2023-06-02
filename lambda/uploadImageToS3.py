import boto3
import json

s3 = boto3.client('s3')

def lambda_handler(event, context):


    bucket_name = 'minipax-image-bucket-fit5225'
    object_key = 'image/'+ event['name']
    object_data = event['value']

    # Write the object to S3
    s3.put_object(Bucket=bucket_name, Key=object_key, Body=object_data)

    return {
        'statusCode': 200,
        'body': 'upload image successful'
    }