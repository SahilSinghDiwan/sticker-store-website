import boto3
import os
from werkzeug.utils import secure_filename
from botocore.exceptions import ClientError

s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
    aws_secret_access_key=os.getenv('AWS_SECRET_KEY'),
    region_name=os.getenv('AWS_REGION', 'us-east-1')
)

def upload_file_to_s3(file, bucket_name=os.getenv('S3_BUCKET')):
    """Upload a file to S3 bucket"""
    try:
        filename = secure_filename(file.filename)
        s3_client.upload_fileobj(
            file,
            bucket_name,
            filename,
            ExtraArgs={'ACL': 'public-read'}
        )
        return f"https://{bucket_name}.s3.amazonaws.com/{filename}"
    except ClientError as e:
        raise Exception(f"S3 upload error: {str(e)}")

# Make sure to create __init__.py in the services directory 