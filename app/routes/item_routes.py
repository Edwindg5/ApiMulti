from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from typing import List
from logging import getLogger
from app.models.items import Item
from app.models.users import User
from app.models.categories import Category
from app.schemas.items import ItemCreate, ItemResponse, UpdateItem,UpdateItemByUser
from app.shared.config.db import get_db
from app.shared.middlewares.auth_middleware import get_current_user


logger = getLogger(__name__)

router = APIRouter(prefix="/items", tags=["Items"])


# Crear un artículo
@router.post("/", response_model=ItemResponse, status_code=201)
def crear_item(item: ItemCreate, db: Session = Depends(get_db)):
    if item.usuario_id is None:
        raise HTTPException(status_code=400, detail="El campo usuario_id es obligatorio.")
    
    user = db.query(User).filter(User.id_usuario == item.usuario_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="El usuario asociado no existe.")
    
    category = db.query(Category).filter(Category.id_categoria == item.id_categoria).first()
    if not category:
        raise HTTPException(status_code=404, detail="La categoría asociada no existe.")
    
    if item.url_imagen is None:
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
            url_imagen=item.url_imagen,  # Correct field name
            cantidad=item.cantidad
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


@router.put("/{item_id}", response_model=ItemResponse)
def actualizar_item(item_id: int, item_update: UpdateItem, db: Session = Depends(get_db)):
    try:
        # Verificar si el artículo existe
        db_item = db.query(Item).filter(Item.id_articulo == item_id).first()
        if not db_item:
            raise HTTPException(status_code=404, detail="Artículo no encontrado")

        # Validar que la categoría existe si se proporciona un `id_categoria`
        if item_update.id_categoria is not None:
            category = db.query(Category).filter(Category.id_categoria == item_update.id_categoria).first()
            if not category:
                raise HTTPException(status_code=404, detail="La categoría asociada no existe.")

        # Actualizar solo los campos enviados en el cuerpo de la solicitud
        updated_fields = item_update.dict(exclude_unset=True)
        for key, value in updated_fields.items():
            setattr(db_item, key, value)

        # Guardar los cambios
        db.commit()
        db.refresh(db_item)
        return db_item

    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error de integridad en la base de datos: {str(e)}")
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error del servidor: {str(e)}")


from sqlalchemy.orm import joinedload
from fastapi import Query

@router.get("/", response_model=List[ItemResponse])
async def get_all_items_by_user(id_user: int, db: Session=Depends(get_db)):
    try:
        # Obtener artículos por usuario con detalles del usuario
        items = (
            db.query(Item)
            .options(joinedload(Item.user))  # Carga las relaciones
            .filter(Item.usuario_id == id_user)
            .all()
        )
        return items
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener artículos: {e}")
        raise HTTPException(status_code=500, detail="Error del servidor.")

#searchbynameitems, utilizando %like%
@router.get("/search_by_name", response_model=List[ItemResponse])
async def search_item_by_name(
    name: str = Query(..., min_length=1, description="Nombre del artículo a buscar"),
    db: Session = Depends(get_db)
):
    try:
        items = (
            db.query(Item)
            .options(joinedload(Item.user))  # Solo cargamos la relación necesaria
            .filter(Item.nombre_articulo.ilike(f"%{name}%"))  # Coincidencia parcial
            .all()
        )

        # Verificar si no hay resultados
        if not items:
            raise HTTPException(
                status_code=404,
                detail=f"No se encontraron artículos que coincidan con: '{name}'"
            )

        # Retornar los artículos encontrados
        return items

    except SQLAlchemyError as e:
        logger.error(f"Error al buscar artículos: {e}")
        raise HTTPException(status_code=500, detail="Error del servidor.")


#itemsbyuser 

@router.get("/by_user/{id_user}", response_model=List[ItemResponse])
async def get_items_by_user(id_user: int, db: Session = Depends(get_db)):
    try:
        # Obtener artículos por usuario
        items = (
            db.query(Item)
            .options(joinedload(Item.user)) 
            .filter(Item.usuario_id == id_user)
            .all()
        )
        # Verificar si no hay resultados
        if not items:
            raise HTTPException(
                status_code=404,
                detail=f"No se encontraron artículos asociados al usuario con ID: {id_user}"
            )
        # Retornar los artículos encontrados
        return items
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener artículos: {e}")
        raise HTTPException(status_code=500, detail="Error del servidor.")
    
    
@router.get("/search", response_model=List[dict])
async def search_items(
    query: str = Query(..., min_length=1, description="Letra inicial o nombre completo del artículo"),
    db: Session = Depends(get_db)
):
    try:
        # Buscar artículos que comiencen con la letra o coincidan con el texto completo
        items = (
            db.query(Item)
            .options(joinedload(Item.user))  # Solo cargamos la relación necesaria
            .filter(Item.nombre_articulo.ilike(f"{query}%"))  # Coincidencia inicial
            .all()
        )

        # Verificar si no hay resultados
        if not items:
            raise HTTPException(
                status_code=404,
                detail=f"No se encontraron artículos que coincidan con: '{query}'"
            )

        # Crear la respuesta solo con los campos necesarios
        response = [
            {
                "nombre_articulo": item.nombre_articulo,
                "url_imagen": item.url_imagen,
                "nombre_usuario": item.user.nombre if item.user else None
            }
            for item in items
        ]

        return response

    except SQLAlchemyError as e:
        logger.error(f"Error al buscar artículos: {e}")
        raise HTTPException(status_code=500, detail="Error del servidor.")
    
    
    
    
    
@router.get("/all", response_model=List[ItemResponse])
def get_all_items(db: Session = Depends(get_db)):
    try:
        items = (
            db.query(Item)
            .options(joinedload(Item.user), joinedload(Item.categoria))
            .all()
        )
        if not items:
            raise HTTPException(status_code=404, detail="No se encontraron artículos registrados.")
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al obtener los artículos.")



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


# Eliminar un artículo
@router.delete("/{item_id}", status_code=200)
def eliminar_item(
    item_id: int, 
    db: Session = Depends(get_db), 
):
    item = db.query(Item).filter(Item.id_articulo == item_id).first()
    db.delete(item)
    db.commit()
    return {"message": "Artículo eliminado exitosamente"}


# Obtener artículos por categoríafrom sqlalchemy.orm import joinedload

@router.get("/categories/{category_id}/items", response_model=List[ItemResponse])
def get_items_by_category(category_id: int, db: Session = Depends(get_db)):
    try:
        # Query para obtener artículos por categoría con detalles del usuario
        items = (
            db.query(Item)
            .options(joinedload(Item.user), joinedload(Item.categoria))
            .filter(Item.id_categoria == category_id)
            .all()
        )
        if not items:
            raise HTTPException(status_code=404, detail="No se encontraron artículos para esta categoría")
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al obtener los artículos.")