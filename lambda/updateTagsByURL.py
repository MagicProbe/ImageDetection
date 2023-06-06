import json
import boto3
import uuid
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table_name = 'images'
table = dynamodb.Table(table_name)


def lambda_handler(event, context):
    body = json.loads(event['body'])
    url = body['url']
    type = body['type']
    tags = body['tags']

    username = event['requestContext']['authorizer']['claims']['cognito:username']

    tags = json.loads(tags)

    # print(tags)

    param_username = url.replace("https://minipax-image-bucket-fit5225.s3.amazonaws.com/", "").split("/")[0]
    if username != param_username:
        return {
            'statusCode': 400,
            'body': json.dumps('Unauthorized!')
        }

    if type == '1':  # 添加标签
        for tag in tags:
            tag_name = tag['name']
            tag_count = tag.get('count', 1)

            response = table.query(
                IndexName='S3URL-tag-index',
                KeyConditionExpression=Key('S3URL').eq(url) & Key('tag').eq(tag_name)
            )

            if len(response['Items']) > 0:
                item = response['Items'][0]
                table.update_item(
                    Key={'id': item['id']},
                    UpdateExpression="set #count=#count + :val",
                    ExpressionAttributeNames={'#count': 'count'},
                    ExpressionAttributeValues={
                        ':val': int(tag_count)
                    }
                )
            else:
                data = {
                    'id': str(uuid.uuid4()),
                    'S3URL': url,
                    'tag': tag_name,
                    'username': username,
                    'count': tag_count
                }
                response = table.put_item(Item=data)

    elif type == '0':  # 删除标签
        for tag in tags:
            tag_name = tag['name']
            tag_count = tag.get('count', 1)

            response = table.query(
                IndexName='S3URL-tag-index',
                KeyConditionExpression=Key('S3URL').eq(url) & Key('tag').eq(tag_name)
            )

            if len(response['Items']) > 0:
                item = response['Items'][0]

                if item['count'] < tag_count:
                    table.delete_item(
                        Key={'id': item['id']}
                    )
                else:
                    table.update_item(
                        Key={'id': item['id']},
                        UpdateExpression="set #count=#count - :val",
                        ExpressionAttributeNames={'#count': 'count'},
                        ExpressionAttributeValues={
                            ':val': int(tag_count)
                        }
                    )

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps('update successful!')
    }
