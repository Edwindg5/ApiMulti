from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ShoppingCart(Base):
    __tablename__ = 'shopping_cart'

    id_shopping_cart = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey('users.id_usuario'))
    articulo_id = Column(Integer, ForeignKey('items.id_articulo'))
    cantidad = Column(Integer, nullable=False)
    fecha_agregado = Column(TIMESTAMP, server_default=func.current_timestamp())
