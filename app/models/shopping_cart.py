# Modelo ShoppingCart
from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.shared.config.db import Base


class ShoppingCart(Base):
    __tablename__ = 'shopping_cart'

    id_shopping_cart = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey('users.id_usuario'), nullable=False)
    articulo_id = Column(Integer, ForeignKey('items.id_articulo'), nullable=False)
    cantidad = Column(Integer, nullable=False)
    fecha_agregado = Column(TIMESTAMP, server_default=func.current_timestamp())

    # Relaciones
    articulo = relationship("Item", back_populates="shopping_cart")
    user = relationship("User", back_populates="shopping_cart")  # Cambiar 'users' a 'user'
