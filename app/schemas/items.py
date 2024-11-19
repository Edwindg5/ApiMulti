from pydantic import BaseModel
from typing import Optional, Literal
from datetime import datetime

class ItemCreate(BaseModel):
    nombre_articulo: str
    descripcion: Optional[str]
    id_categoria: int
    precio: float
    tipo_transaccion: Literal['COMPRA', 'VENTA', 'INTERCAMBIO', 'PRESTAMO']  # Opciones válidas
    usuario_id: int
    estado: Literal[
        'PENDING', 'COMPLETED', 'CANCELLED', 'VENTA', 'INTERCAMBIO',
        'DONACIÓN', 'DISPONIBLE', 'NO_DISPONIBLE', 'ELIMINADO', 'COMPRA'
    ]  # Opciones válidas para el estado

class ItemResponse(ItemCreate):
    id_articulo: int
    fecha_publicacion: datetime  # Validación para mantener solo la fecha

    class Config:
        orm_mode = True
