import boto3

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # 获取上传的文件对象和存储桶名称
    file_obj = event['Records'][0]['s3']
    bucket_name = file_obj['bucket']['name']
    file_path = file_obj['object']['key']

    # 将文件存储到 S3 存储桶中
    s3.put_object(Body=file_path, Bucket=bucket_name, Key=file_path)

    return {
        'statusCode': 200,
        'body': 'File uploaded successfully.'
    }