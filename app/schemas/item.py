from pydantic import BaseModel
from typing import Optional
from app.utils.security import TransactionStatus

class ItemBase(BaseModel):
    nombre_articulo: str
    descripcion: Optional[str] = None
    categoria_id: int
    precio: float
    tipo_transaccion: Optional[TransactionStatus] = None
    usuario_id: int
    estado: Optional[TransactionStatus] = None

class ItemCreate(ItemBase):
    pass

class ItemResponse(ItemBase):
    id_articulo: int
    fecha_publicacion: str

    class Config:
        orm_mode = True
