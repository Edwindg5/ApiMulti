from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from typing import List
from logging import getLogger
from app.models.items import Item
from app.models.users import User
from app.models.categories import Category
from app.schemas.items import ItemCreate, ItemResponse, UpdateItem
from app.shared.config.db import get_db
import boto3
import os
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import uuid

logger = getLogger(__name__)
    
router = APIRouter(prefix="/items", tags=["Items"])

# Configuración de AWS S3
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_SECRET_SESSION_TOKEN = os.getenv("AWS_SECRET_SESSION_TOKEN")
AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")
AWS_REGION = os.getenv("AWS_REGION")

s3 = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    aws_session_token=AWS_SECRET_SESSION_TOKEN,  # Solo si es temporal
    region_name=AWS_REGION
)

try:
    response = s3.list_buckets()
    print("Buckets disponibles:", response['Buckets'])
except Exception as e:
    print("Error al conectar a S3:", str(e))

@router.post("/", response_model=ItemResponse, status_code=201)
async def crear_item(
    nombre_articulo: str = Form(...),
    descripcion: str = Form(None),
    id_categoria: int = Form(...),
    precio: float = Form(...),
    tipo_transaccion: str = Form(...),
    usuario_id: int = Form(...),
    estado: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    try:
        # Validar archivo
        if not file or file.filename == "":
            raise HTTPException(status_code=400, detail="No se envió un archivo válido.")
        file_content = await file.read()
        if not file_content:
            raise HTTPException(status_code=400, detail="El archivo está vacío.")

        # Validar usuario
        user = db.query(User).filter(User.id_usuario == usuario_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="El usuario asociado no existe.")

        # Validar categoría
        category = db.query(Category).filter(Category.id_categoria == id_categoria).first()
        if not category:
            raise HTTPException(status_code=404, detail="La categoría asociada no existe.")

        # Generar clave única para el archivo
        file_key = f"uploads/{uuid.uuid4().hex}_{file.filename}"

        # Subir archivo a S3
        s3.put_object(Bucket=AWS_BUCKET_NAME, Key=file_key, Body=file_content)

        # Generar URL pública del archivo
        file_url = f"https://{AWS_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{file_key}"

        # Crear el artículo
        db_item = Item(
            nombre_articulo=nombre_articulo,
            descripcion=descripcion,
            id_categoria=id_categoria,
            precio=precio,
            tipo_transaccion=tipo_transaccion,
            usuario_id=usuario_id,
            estado=estado,
            image_url=file_url,  # Asignar la URL de la imagen al artículo
        )
        db.add(db_item)
        db.commit()
        db.refresh(db_item)

        # Cargar relaciones para devolver la respuesta completa
        db_item.user = user
        db_item.categoria = category

        return db_item

    except NoCredentialsError as e:
        raise HTTPException(status_code=500, detail="Credenciales de AWS no configuradas correctamente.")
    except PartialCredentialsError as e:
        raise HTTPException(status_code=500, detail="Credenciales incompletas para AWS.")
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error de integridad en la base de datos.")
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error del servidor al crear el artículo.")
    except Exception as e:
        db.rollback()
        logger.exception("Error inesperado al crear el artículo.")
        raise HTTPException(status_code=500, detail=f"Error al procesar la solicitud: {str(e)}")

@router.get("/{item_id}", response_model=ItemResponse)
def leer_item(item_id: int, db: Session = Depends(get_db)):
    item = (
        db.query(Item)
        .options(joinedload(Item.user), joinedload(Item.categoria))  # Cargar relaciones
        .filter(Item.id_articulo == item_id)
        .first()
    )
    if not item:
        raise HTTPException(status_code=404, detail="Artículo no encontrado")
    return item


@router.put("/{item_id}", response_model=ItemResponse)
def actualizar_item(item_id: int, item_update: UpdateItem, db: Session = Depends(get_db)):
    try:
        db_item = db.query(Item).filter(Item.id_articulo == item_id).first()
        if not db_item:
            raise HTTPException(status_code=404, detail="Artículo no encontrado")

        updated_fields = item_update.dict(exclude_unset=True)
        for key, value in updated_fields.items():
            setattr(db_item, key, value)

        db.commit()
        db.refresh(db_item)
        return db_item
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error de integridad en la base de datos.")
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error del servidor.")


@router.delete("/{item_id}", status_code=200)
def eliminar_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id_articulo == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Artículo no encontrado")

    db.delete(item)
    db.commit()
    return {"message": "Artículo eliminado exitosamente"}


@router.get("/categories/{category_id}/items", response_model=List[ItemResponse])
def get_items_by_category(category_id: int, db: Session = Depends(get_db)):
    items = (
        db.query(Item)
        .options(joinedload(Item.user), joinedload(Item.categoria))  # Asegura la carga de relaciones
        .filter(Item.id_categoria == category_id)
        .all()
    )
    if not items:
        raise HTTPException(status_code=404, detail="No se encontraron artículos para esta categoría")
    return items
