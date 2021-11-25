import boto3, uuid

class MyS3Client:
    def __init__(self, aws_access_key_id, aws_secret_access_key, bucket_name):
        boto3_s3 = boto3.client(
            's3',
            aws_access_key_id     = aws_access_key_id,
            aws_secret_access_key = aws_secret_access_key
        )
        self.s3_client = boto3_s3
        self.bucket_name = bucket_name

    def upload(self, file):
        file_name = str(uuid.uuid4())

        self.s3_client.upload_fileobj(
            file, 
            self.bucket_name,
            file_name,
            ExtraArgs={"ContentType": file.content_type}
        )

        return f'https://{self.bucket_name}.s3.ap-northeast-2.amazonaws.com/{file_name}'