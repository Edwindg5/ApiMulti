from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.models.items import Item
from app.models.users import User
from app.schemas.items import ItemCreate, ItemResponse
from app.shared.config.db import get_db
from app.models.categories import Category
from logging import getLogger

logger = getLogger(__name__)

router = APIRouter(prefix="/items")

@router.post("/", response_model=ItemResponse)
def crear_item(item: ItemCreate, db: Session = Depends(get_db)):
    try:
        # Validar usuario
        user = db.query(User).filter(User.id_usuario == item.usuario_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="El usuario asociado no existe.")
        
        # Validar categoría
        category = db.query(Category).filter(Category.id_categoria == item.id_categoria).first()
        if not category:
            raise HTTPException(status_code=404, detail="La categoría asociada no existe.")
        
        # Crear el artículo
        db_item = Item(**item.dict())
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Error de integridad al insertar: {e}")
        raise HTTPException(status_code=400, detail="Error de integridad en la base de datos.")
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error general de SQLAlchemy: {e}")
        raise HTTPException(status_code=500, detail=f"Error del servidor: {str(e)}")


@router.get("/{item_id}", response_model=ItemResponse)
def leer_item(item_id: int, db: Session = Depends(get_db)):
    # Buscar artículo por ID
    item = db.query(Item).filter(Item.id_articulo == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Artículo no encontrado")
    return item


@router.delete("/{item_id}")
def eliminar_item(item_id: int, db: Session = Depends(get_db)):
    # Buscar y eliminar el artículo
    item = db.query(Item).filter(Item.id_articulo == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Artículo no encontrado")
    db.delete(item)
    db.commit()
    return {"message": "Artículo eliminado exitosamente"}
