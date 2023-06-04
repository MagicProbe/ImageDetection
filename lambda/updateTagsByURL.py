import json
import boto3
import uuid

dynamodb = boto3.resource('dynamodb')

table_name = 'images'

def lambda_handler(event, context):

    url = event['url']
    type = event['type']
    tags = event['tags']



    if type == 1:  # 添加标签
        for tag in tags:
            tag_name = tag['tag']
            tag_count = tag.get('count', 1)
            for i in range(tag_count):
                data = {}
                data['id'] = {'S': str(uuid.uuid4())}
                data['name'] = {'S': url[url.index('image/'):]}
                data['tags'] = {'S': tag_name}
                data['S3URL'] = {'S': url}
                response = dynamodb.put_item(TableName=table_name, Item=data)
    elif type == 0:  # 删除标签
        for tag in tags:
            tag_name = tag['tag']
            tag_count = tag.get('count', 1)

            table = dynamodb.Table(table_name)
            response = table.scan(FilterExpression='contains(#tags, :val)',
                                  ExpressionAttributeNames={'#tags': 'tags'},
                                  ExpressionAttributeValues={':val': tag_name})

            with table.batch_writer() as batch:
                for i in range(min(tag_count, len(response['Items']))):
                    batch.delete_item(Key={'id': response['Items'][i]['id']})


    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
