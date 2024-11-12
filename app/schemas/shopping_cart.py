from pydantic import BaseModel

class ShoppingCartBase(BaseModel):
    usuario_id: int
    articulo_id: int
    cantidad: int

class ShoppingCartCreate(ShoppingCartBase):
    pass

class ShoppingCartResponse(ShoppingCartBase):
    id_shopping_cart: int
    fecha_agregado: str

    class Config:
        orm_mode = True
