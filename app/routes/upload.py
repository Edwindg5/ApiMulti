from fastapi import APIRouter, UploadFile, File, HTTPException 
import boto3
import os
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from dotenv import load_dotenv
from fastapi.responses import StreamingResponse
import io   

router = APIRouter()

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Configuración de AWS S3 desde las variables de entorno
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_SECRET_SESSION_TOKEN = os.getenv("AWS_SECRET_SESSION_TOKEN")  # Token de sesión
AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")
AWS_REGION = os.getenv("AWS_REGION")

# Inicializar cliente de S3 con las credenciales temporales
s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    aws_session_token=os.getenv("AWS_SECRET_SESSION_TOKEN"),
    region_name=os.getenv("AWS_REGION"),
)
@router.post("/upload")
async def upload_file_to_s3(file: UploadFile = File(...)):
    try:
        # Leer el contenido del archivo
        file_content = await file.read()

        # Nombre único para el archivo en S3
        file_key = f"uploads/{file.filename}"

        # Subir el archivo a S3
        s3_client.put_object(Bucket=AWS_BUCKET_NAME, Key=file_key, Body=file_content)

        # Construir la URL pública del archivo en S3
        file_url = f"https://{AWS_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{file_key}"

        return {"message": "File uploaded successfully", "url": file_url}

    except (NoCredentialsError, PartialCredentialsError) as e:
        raise HTTPException(status_code=500, detail="AWS credentials not configured correctly")
    except Exception as e:
        print("AWS_ACCESS_KEY_ID:", os.getenv("AWS_ACCESS_KEY_ID"))
        print("AWS_SECRET_ACCESS_KEY:", os.getenv("AWS_SECRET_ACCESS_KEY"))
        print("AWS_BUCKET_NAME:", os.getenv("AWS_BUCKET_NAME"))
        print("AWS_SECRET_SESSION_TOKEN:", os.getenv("AWS_SECRET_SESSION_TOKEN"))
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    
@router.get("/files")
async def list_files_in_s3():
    try:
        # Listar los objetos en el bucket
        response = s3_client.list_objects_v2(Bucket=AWS_BUCKET_NAME)

        # Verificar si hay archivos en el bucket
        if 'Contents' not in response:
            raise HTTPException(status_code=404, detail="No files found in the bucket")

        # Obtener los nombres de los archivos y generar las URL públicas
        file_urls = [
            f"https://{AWS_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{file['Key']}"
            for file in response['Contents']
        ]

        return {"files": file_urls}

    except (NoCredentialsError, PartialCredentialsError) as e:
        raise HTTPException(status_code=500, detail="AWS credentials not configured correctly")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    
@router.get("/files/{filename}")
async def get_file_from_s3(filename: str):
    try:
        # Obtener el archivo de S3
        response = s3_client.get_object(Bucket=AWS_BUCKET_NAME, Key=filename)

        # Obtener el contenido del archivo
        file_content = response['Body'].read()

        # Crear una respuesta que envíe el archivo
        return StreamingResponse(io.BytesIO(file_content), media_type="application/octet-stream")

    except s3_client.exceptions.NoSuchKey:
        raise HTTPException(status_code=404, detail="File not found")
    except (NoCredentialsError, PartialCredentialsError) as e:
        raise HTTPException(status_code=500, detail="AWS credentials not configured correctly")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
