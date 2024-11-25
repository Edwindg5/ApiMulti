from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from typing import List
from logging import getLogger
from app.models.items import Item
from app.models.users import User
from app.models.categories import Category
from app.schemas.items import ItemCreate, ItemResponse, UpdateItem
from app.shared.config.db import get_db


logger = getLogger(__name__)

router = APIRouter(prefix="/items", tags=["Items"])


# Crear un artículo
@router.post("/", response_model=ItemResponse, status_code=201)
def crear_item(item: ItemCreate, db: Session = Depends(get_db)):
    # Validar usuario y categoría
    if item.usuario_id is None:
        raise HTTPException(status_code=400, detail="El campo usuario_id es obligatorio.")
    
    user = db.query(User).filter(User.id_usuario == item.usuario_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="El usuario asociado no existe.")
    
    category = db.query(Category).filter(Category.id_categoria == item.id_categoria).first()
    if not category:
        raise HTTPException(status_code=404, detail="La categoría asociada no existe.")
    
    # Validar imagen y cantidad
    if item.imagen_url is None:
        raise HTTPException(status_code=400, detail="La URL de la imagen es obligatoria.")
    
    try:
        db_item = Item(
            nombre_articulo=item.nombre_articulo,
            descripcion=item.descripcion,
            id_categoria=item.id_categoria,
            precio=item.precio,
            tipo_transaccion=item.tipo_transaccion,
            usuario_id=item.usuario_id,
            estado=item.estado,
            url_imagen=item.imagen_url,
            cantidad=item.cantidad  # Se guarda la cantidad
        )
        
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        db_item.user = user
        db_item.categoria = category
        return db_item
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error de integridad en la base de datos.")
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error del servidor.")



    
from sqlalchemy.orm import joinedload


@router.post("/verify", status_code=200)
def verify_user(name: str, email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.nombre == name, User.email == email).first()

    if user:
        return {"authenticated": True, "user_id": user.id_usuario}
    else:
        raise HTTPException(status_code=401, detail="Usuario no autenticado")


@router.get("/{item_id}", response_model=ItemResponse)
def leer_item(item_id: int, db: Session = Depends(get_db)):
    item = (
        db.query(Item)
        .options(joinedload(Item.user), joinedload(Item.categoria))  # Carga las relaciones
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


# Eliminar un artículo por ID
@router.delete("/{item_id}", status_code=200)
def eliminar_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id_articulo == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Artículo no encontrado")

    db.delete(item)
    db.commit()
    return {"message": "Artículo eliminado exitosamente"}



# Obtener artículos por categoríafrom sqlalchemy.orm import joinedload


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