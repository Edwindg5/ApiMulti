from pydantic import BaseModel
from typing import Optional, Literal
from datetime import datetime
from app.schemas.categories import CategoryResponse
from app.schemas.user import UserResponse
from typing import List

class ItemCreate(BaseModel):
    nombre_articulo: str
    descripcion: Optional[str] = None
    id_categoria: int
    precio: float
    tipo_transaccion: Literal['COMPRA', 'VENTA', 'INTERCAMBIO', 'PRESTAMO']
    usuario_id: int
    estado: Literal['PENDING', 'COMPLETED', 'CANCELLED', 'DISPONIBLE', 'NO_DISPONIBLE', 'ELIMINADO']
    url_imagen: Optional[str] = None  # Ajustado el nombre
    cantidad: int = 0

class UpdateItem(BaseModel):
    nombre_articulo: Optional[str] = None
    descripcion: Optional[str] = None
    id_categoria: Optional[int] = None
    precio: Optional[float] = None
    tipo_transaccion: Optional[Literal['COMPRA', 'VENTA', 'INTERCAMBIO', 'PRESTAMO']] = None
    usuario_id: Optional[int] = None
    estado: Optional[Literal['PENDING', 'COMPLETED', 'CANCELLED', 'DISPONIBLE', 'NO_DISPONIBLE', 'ELIMINADO']] = None
    url_imagen: Optional[str] = None
    cantidad: Optional[int] = None

class ItemResponse(ItemCreate):
    id_articulo: int
    fecha_publicacion: datetime
    categoria: Optional[CategoryResponse] = None
    user: Optional[UserResponse] = None

    class Config:
        orm_mode = True

