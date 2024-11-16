from pydantic import BaseModel, validator
from datetime import datetime

class ShoppingCartBase(BaseModel):
    usuario_id: int
    articulo_id: int
    cantidad: int

class ShoppingCartCreate(ShoppingCartBase):
    pass

class ShoppingCartResponse(ShoppingCartBase):
    id_shopping_cart: int
    fecha_agregado: str  # Se mantiene como string

    @validator("fecha_agregado", pre=True)
    def format_fecha_agregado(cls, value):
        if isinstance(value, datetime):
            return value.isoformat()  # Convierte datetime a string en formato ISO 8601
        return value

    class Config:
        orm_mode = True
