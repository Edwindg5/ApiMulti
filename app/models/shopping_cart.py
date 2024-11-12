from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey
from app.shared.config.db import Base
from sqlalchemy.sql import func

class ShoppingCart(Base):
    __tablename__ = "shopping_cart"

    id_shopping_cart = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("users.id_usuario"))
    articulo_id = Column(Integer, ForeignKey("items.id_articulo"))
    cantidad = Column(Integer, nullable=False)
    fecha_agregado = Column(TIMESTAMP, server_default=func.now())
