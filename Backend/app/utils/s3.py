import os
import boto3
from werkzeug.utils import secure_filename
from flask import current_app
from typing import BinaryIO

def get_s3_client():
    """Create and return an S3 client using credentials from config."""
    return boto3.client(
        's3',
        aws_access_key_id=current_app.config['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=current_app.config['AWS_SECRET_ACCESS_KEY'],
        region_name=current_app.config['AWS_REGION']
    )

def upload_file_to_s3(file: BinaryIO, folder: str = "uploads") -> str:
    """
    Upload a file to S3 bucket
    
    Args:
        file: File object to upload
        folder: The folder name in the bucket (default: "uploads")
    
    Returns:
        str: The URL of the uploaded file
    """
    try:
        filename = secure_filename(file.filename)
        # Create unique filename using timestamp
        unique_filename = f"{folder}/{os.urandom(8).hex()}_{filename}"
        
        s3_client = get_s3_client()
        bucket_name = current_app.config['AWS_BUCKET_NAME']
        
        # Upload file
        s3_client.upload_fileobj(
            file,
            bucket_name,
            unique_filename,
            ExtraArgs={
                'ContentType': file.content_type
            }
        )
        
        # Generate URL
        url = f"https://{bucket_name}.s3.{current_app.config['AWS_REGION']}.amazonaws.com/{unique_filename}"
        return url
        
    except Exception as e:
        current_app.logger.error(f"Error uploading file to S3: {str(e)}")
        raise 