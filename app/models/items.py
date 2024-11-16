from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from app.shared.config.db import Base


class Item(Base):
    __tablename__ = 'items'

    id_articulo = Column(Integer, primary_key=True, autoincrement=True)
    nombre_articulo = Column(String(100), nullable=False)
    descripcion = Column(String(255), nullable=True)
    categoria_id = Column(Integer, nullable=False)
    precio = Column(Integer, nullable=False)
    tipo_transaccion = Column(String(50), nullable=False)
    usuario_id = Column(Integer, ForeignKey("users.id_usuario"), nullable=False)
    estado = Column(String(50), nullable=False)
    fecha_publicacion = Column(TIMESTAMP, server_default=func.current_timestamp())

    # Relación con User
    user = relationship("User", back_populates="items")

    # Relación con ShoppingCart
    shopping_cart = relationship("ShoppingCart", back_populates="articulo")
    
    # Relación con TransactionHistory
    transactions = relationship("TransactionHistory", back_populates="item")

    # Relaciones con Trade
    trades_solicitados = relationship(
        "Trade",
        foreign_keys="Trade.articulo_solicitado_id",
        back_populates="articulo_solicitado"
    )
    trades_ofrecidos = relationship(
        "Trade",
        foreign_keys="Trade.articulo_ofrecido_id",
        back_populates="articulo_ofrecido"
    )
