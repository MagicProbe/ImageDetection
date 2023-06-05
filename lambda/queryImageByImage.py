# import base64
import json
# from io import BytesIO
import boto3

# Get the service resource.
database = boto3.resource('dynamodb')

def lambda_handler(event, context):

    
    even = json.loads(event)
    imagecode = even['image']
    
    #我是按照下面参考的代码写的 这里有一点对图形数据的处理 我改了一下
    #想了想还是全部注掉了
    # Decode the image from base64
    # im_bytes = base64.b64decode(imagecode)
    # im_file = BytesIO(im_bytes)
    
    # Perform further processing on the image as per your requirements
    # ...

    # Get the tags associated with the image
    queryTags = even['tags']
    
    # Retrieve data from the DynamoDB table
    table = database.Table('LabelDetected')
    response = table.scan()
    dbdata = response['Items']
    imageURL = []

    # Loop over the database items
    for index, element in enumerate(dbdata):
        url = element['URL']
        #
        tags = element['Tags']
        #
        imageInDatabase = set(tags)
        queryFromUser = set(queryTags)

        # If user's query matches one image's JSON object, append this image URL to the list
        # If user's query input is an empty list, then ALL URLs in the database will be returned
        if queryFromUser == imageInDatabase:
            imageURL.append(url)

    result = {}
    if len(imageURL) > 0:
        result["links"] = imageURL
        jsonResult = json.dumps(result)
        return jsonResult
    else:
        return "There are no matching images."

# 下面是找的参考代码  
#  def lambda_handler(event, context):
#     even = json.loads(event)
#     imagecode = even['image']
#     # imagecode = event['image']

#     queryTags = Start_detection(imagecode)    这里他是在这之前把detection这些也写在了里面 
#     # print(queryTags)

#     table = database.Table('LabelDetected')

#     # response = table.query(
#     #     KeyConditionExpression=Key('Tags').eq(queryTags)
#     # )
#     # return response['Items']

#     response = table.scan()
#     dbdata = response['Items']
#     imageURL = []

#     # Loop over the database items
#     for index, element in enumerate(dbdata):

#         url = element['URL']
#         print(url)
#         tags = element['Tags']
#         imageInDatabase = set(tags)
#         # print(imageInDatabase)
#         # print(url)

#         queryFromUser = set(queryTags)
#         # print(queryFromUser)
#         # print(queryTags)

#         # If user's query match one image's JSON object, append this image to the list
#         # If user's query input is an empty list, then ALL url in the database will be returned
#         if queryFromUser == imageInDatabase:
#             imageURL.append(url)

#     result = {}
#     if len(imageURL) > 0:
#         result["links"] = imageURL
#         jsonResult = json.dumps(result)
#         return jsonResult
#     else:
#         return "There is no match images."