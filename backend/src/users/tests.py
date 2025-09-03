from django.test import TestCase
import boto3
import os
from dotenv import load_dotenv
import mimetypes

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')

def upload_to_s3(file_path, bucket_name):
    s3 = boto3.client(
        's3',
        aws_secret_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )
    file_name = os.path.basename(file_path)
    content_type, _ = mimetypes.guess_type(file_path)

    if content_type is None:
        content_type = 'application/octet-stream'

    with open(file_path, 'rb') as file:
        