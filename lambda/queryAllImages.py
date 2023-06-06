import boto3
import json
from boto3.dynamodb.conditions import Key

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

bucket_name = 'minipax-image-bucket-fit5225'
table_name = 'images'
table = dynamodb.Table(table_name)


def lambda_handler(event, context):
    username = event['requestContext']['authorizer']['claims']['cognito:username']

    response = s3.list_objects_v2(
        Bucket=bucket_name,
        Prefix=username + '/image/',
    )

    image_contents = []
    if 'Contents' in response:
        for obj in response['Contents']:
            object_key = obj['Key']
            object_response = s3.get_object(Bucket=bucket_name, Key=object_key)
            object_content = object_response['Body'].read()

            response = table.query(
                IndexName='S3URL-tag-index',
                KeyConditionExpression=Key('S3URL').eq(
                    'https://minipax-image-bucket-fit5225.s3.amazonaws.com/' + object_key)
            )

            tags = {}
            with table.batch_writer() as batch:
                if 'Items' in response:
                    for item in response['Items']:
                        tags[item['tag']] = int(item['count'])

            # print(tags)
            image_info = {
                'S3URL': 'https://minipax-image-bucket-fit5225.s3.amazonaws.com/' + object_key,
                'name': object_key.split('/')[-1],
                'tags': tags
                # 'value': object_content
            }
            # print(image_info['value'])

            image_contents.append(image_info)

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(image_contents)
    }
