import boto3
import json

dynamodb = boto3.resource('dynamodb')

table_name = 'images'

# def lambda_handler(event, context):
#     table = dynamodb.Table(table_name)
#     tags = event['tags']
#     for obj in tags:
#         tag = obj['tag']
#         count = obj['count']

#         response = table.scan(FilterExpression='contains(#tags, :val)',
#                           ExpressionAttributeNames={'#tags': 'tags'},
#                           ExpressionAttributeValues={':val': tag})

#         ans = []
#         for item in response['Items']:
#             ans.append()


#     return {
#         'statusCode': 200,
#         'body': 'delete successful'
#     }


# 这里我用的是json.loads 传入的 不知道会不会有bug
def lambda_handler(event, context):
    imageURL = []
    # Receive user's query JSON
    even = json.loads(event)
    queryTags = even['tags'] 
    table = dynamodb.Table('LabelDetected')

    response = table.scan()
    dbdata = response['Items']

    # Loop over the database items
    for index, element in enumerate(dbdata):
        
        url = element['URL']
        tags = element['Tags']
        imageInDatabase = set(tags)
        # print(imageInDatabase)
        # print(url)
        
        queryFromUser = set(queryTags)
        
        if len(queryTags) == 0:
            imageURL.append(url)
        else:
            if queryFromUser == imageInDatabase:
                imageURL.append(url)
    
    result = {"links": imageURL}
    jsonResult = json.dumps(result)
# 输出我也改了一下 不太确定 再看看
    return jsonResult
