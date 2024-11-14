from pydantic import BaseModel
from datetime import date

class ItemBase(BaseModel):
    nombre_articulo: str
    descripcion: str
    categoria_id: int
    precio: float
    tipo_transaccion: str
    usuario_id: int
    estado: str
    fecha_publicacion: date

class ItemCreate(ItemBase):
    pass

class ItemResponse(ItemBase):
    id_articulo: int

    class Config:
        from_attributes = True  # Compatibilidad con Pydantic v2
