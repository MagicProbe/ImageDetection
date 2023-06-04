import json
import boto3

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

bucket_name = 'minipax-image-bucket-fit5225'
table_name = 'images'


def lambda_handler(event, context):
    response = s3.list_objects_v2(
        Bucket=bucket_name,
        Prefix='image/',
    )

    image_contents = []
    if 'Contents' in response:
        for obj in response['Contents']:
            object_key = obj['Key']
            object_response = s3.get_object(Bucket=bucket_name, Key=object_key)
            object_content = object_response['Body'].read()

            table = dynamodb.Table(table_name)
            response = table.scan(FilterExpression='contains(#name, :val)',
                                  ExpressionAttributeNames={'#name': 'name'},
                                  ExpressionAttributeValues={':val': object_key})
            # print(response)

            tags = {}
            with table.batch_writer() as batch:
                for item in response['Items']:
                    if item['tags'] in tags:
                        tags[item['tags']] += 1
                    else:
                        tags[item['tags']] = 1

            # print(tags)
            # 解析对象内容并组织成指定格式的字典
            image_info = {
                'S3URL': f'https://{bucket_name}.s3.amazonaws.com/{object_key}',
                'tags': tags,
                'name': object_key.split('/')[-1],
                'value': object_content
            }
            print(image_info['value'])

            image_contents.append(image_info)

    return {
        'statusCode': 200,
        'body': image_contents
    }
