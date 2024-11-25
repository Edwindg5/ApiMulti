from pydantic import BaseModel
from typing import Optional, Literal
from datetime import datetime
from app.schemas.categories import CategoryResponse
from app.schemas.user import UserResponse

class ItemCreate(BaseModel):
    nombre_articulo: str
    descripcion: Optional[str] = None
    id_categoria: int
    precio: int
    tipo_transaccion: Literal['COMPRA', 'VENTA', 'INTERCAMBIO', 'PRESTAMO']
    usuario_id: int
    estado: Literal['PENDING', 'COMPLETED', 'CANCELLED', 'DISPONIBLE', 'NO_DISPONIBLE', 'ELIMINADO']
    imagen_url: Optional[str] = None
    cantidad: int  # Agregamos el campo "cantidad"

class UpdateItem(BaseModel):
    nombre_articulo: Optional[str] = None
    descripcion: Optional[str] = None
    categoria_id: Optional[int] = None
    precio: Optional[float] = None
    tipo_transaccion: Optional[str] = None
    usuario_id: Optional[int] = None
    estado: Optional[str] = None
    imagen_url: Optional[str] = None
    cantidad: Optional[int] = None  # También lo agregamos aquí para actualizaciones

class ItemResponse(ItemCreate):
    id_articulo: int
    fecha_publicacion: datetime
    categoria: Optional[CategoryResponse] = None
    user: Optional[UserResponse] = None
    
    class Config:
        orm_mode = True
