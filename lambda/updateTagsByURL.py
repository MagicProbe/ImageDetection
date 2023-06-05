import json
import boto3
import uuid
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table_name = 'images'
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    url = event['url']
    name = url[url.index('image/'):]
    type = event['type']
    tags = event['tags']
    tags = json.loads(tags)

    print(tags)

    if type == '1':  # 添加标签
        for tag in tags:
            tag_name = tag['name']
            tag_count = tag.get('count', 1)

            response = table.query(
                IndexName='name-tag-index',
                KeyConditionExpression=Key('name').eq(name) & Key('tag').eq(tag_name)
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
                    'name': name,
                    'S3URL': url,
                    'tag': tag_name,
                    'count': tag_count
                }
                response = table.put_item(Item=data)

    elif type == '0':  # 删除标签
        for tag in tags:
            tag_name = tag['name']
            tag_count = tag.get('count', 1)

            response = table.query(
                IndexName='name-tag-index',
                KeyConditionExpression=Key('name').eq(name) & Key('tag').eq(tag_name)
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
        'body': json.dumps('update successful!')
    }
