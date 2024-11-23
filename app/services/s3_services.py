import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from fastapi import HTTPException

class S3Service:
    def __init__(self, bucket_name: str, region: str, access_key: str, secret_key: str):
        self.bucket_name = bucket_name
        self.s3_client = boto3.client(
            "s3",
            region_name=region,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
        )

    def upload_file(self, file_obj, file_name: str, folder: str = "uploads"):
        try:
            file_key = f"{folder}/{file_name}"
            self.s3_client.upload_fileobj(
                file_obj,
                self.bucket_name,
                file_key,
                ExtraArgs={"ACL": "public-read", "ContentType": file_obj.content_type},
            )
            file_url = f"https://segundamanoup.s3.us-east-1.amazonaws.com/{file_key}"
            return file_url
        except (NoCredentialsError, PartialCredentialsError):
            raise HTTPException(status_code=500, detail="Error with AWS credentials")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")
