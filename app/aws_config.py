import boto3
import os

def get_aws_credentials_from_secrets(secret_name: str, region_name: str):
    """
    Recupera credenciales desde AWS Secrets Manager.
    """
    client = boto3.client("secretsmanager", region_name=region_name)
    try:
        response = client.get_secret_value(SecretId=secret_name)
        secret_string = response.get("SecretString")
        return eval(secret_string)  # Asegúrate de que el secreto sea un diccionario
    except Exception as e:
        raise RuntimeError(f"Error al obtener el secreto: {str(e)}")

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME", "proyectocuarto")

# Obtener credenciales desde Secrets Manager
secrets = get_aws_credentials_from_secrets("MiSecretName", AWS_REGION)

AWS_CONFIG = {
    "aws_access_key_id": os.getenv("AWS_ACCESS_KEY_ID"),
    "aws_secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
    "aws_session_token": os.getenv("AWS_SESSION_TOKEN"),
    "region_name": os.getenv("AWS_REGION", "us-east-1"),
    "bucket_name": os.getenv("AWS_BUCKET_NAME", "segundamanoup"),
}
