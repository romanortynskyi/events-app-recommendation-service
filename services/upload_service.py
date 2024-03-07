from io import StringIO
import boto3
from botocore.exceptions import ClientError
import os

class UploadService:
  def __init__(self):
    self.s3_client = boto3.client('s3')
    self.bucket = os.environ.get('S3_BUCKET')

  def file_exists(self, key: str) -> bool:
    try:
      self.s3_client.head_object(Bucket = self.bucket, Key = key)

      return True
    
    except ClientError as e:
      if e.response['Error']['Code'] == '404':
        return False
      
      else:
        print(f"Error checking object existence: {e}")

        return False

  def write_text_to_file(self, text: str, key: str):
    string_io = StringIO()
    string_io.write(text)

    response = self.s3_client.put_object(Body=string_io.getvalue(), Bucket = self.bucket, Key = key)

    return response
  
  def read_text_file(self, key: str):
    try:
      response = self.s3_client.get_object(Bucket = self.bucket, Key = key)        
      text_data = response['Body'].read().decode('utf-8')

      return text_data

    except Exception as e:
      return None