import os
from app.services.s3_services import S3Service

def get_s3_service():
    return S3Service(
        bucket_name=os.getenv("S3_BUCKET_NAME"),
        region=os.getenv("AWS_REGION"),
        access_key=os.getenv("AWS_ACCESS_KEY_ID"),
        secret_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )
