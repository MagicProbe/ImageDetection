import boto3
import json
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')

table_name = 'images'
table = dynamodb.Table(table_name)


def lambda_handler(event, context):
    tags = event['tags']
    tags = json.loads(tags)
    result = set()
    for tag in tags:
        single_result = set()
        tag_name = tag['name']
        tag_count = tag.get('count', 1)

        response = table.query(
            IndexName='tag-count-index',
            KeyConditionExpression= '#tag = :tag_name AND #count >= :tag_count',
            ExpressionAttributeNames = {
                '#tag': 'tag',
                '#count': 'count'
            },
            ExpressionAttributeValues = {
                ':tag_name': tag_name,
                ':tag_count': int(tag_count)
            }
        )

        for item in response['Items']:
            single_result.add(item['S3URL'])

        if len(result) == 0:
            result = single_result
        else:
            result = result & single_result

    result = list(result)

    response = []
    for r in result:
        response.append({'S3URL': r})

    return {
        'statusCode': 200,
        'body': response
    }

# 这里我用的是json.loads 传入的 不知道会不会有bug
# def lambda_handler(event, context):
#     imageURL = []
#     # Receive user's query JSON
#     even = json.loads(event)
#     queryTags = even['tags']
#     table = dynamodb.Table('LabelDetected')
#
#     response = table.scan()
#     dbdata = response['Items']
#
#     # Loop over the database items
#     for index, element in enumerate(dbdata):
#
#         url = element['URL']
#         tags = element['Tags']
#         imageInDatabase = set(tags)
#         # print(imageInDatabase)
#         # print(url)
#
#         queryFromUser = set(queryTags)
#
#         if len(queryTags) == 0:
#             imageURL.append(url)
#         else:
#             if queryFromUser == imageInDatabase:
#                 imageURL.append(url)
#
#     result = {"links": imageURL}
#     jsonResult = json.dumps(result)
# # 输出我也改了一下 不太确定 再看看
#     return jsonResult
