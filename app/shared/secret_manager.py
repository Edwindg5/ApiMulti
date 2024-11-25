import boto3

def get_secret(secret_name: str, region_name: str):
    """
    Recupera secretos desde AWS Secrets Manager.
    """
    client = boto3.client("secretsmanager", region_name=region_name)
    try:
        response = client.get_secret_value(SecretId=secret_name)
        return response.get("SecretString")
    except Exception as e:
        raise RuntimeError(f"Error al obtener el secreto: {str(e)}")
