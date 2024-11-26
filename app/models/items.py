from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ENUM
from datetime import date
from app.shared.config.db import Base


class Item(Base):
    __tablename__ = 'items'

    id_articulo = Column(Integer, primary_key=True, autoincrement=True)
    nombre_articulo = Column(String(100), nullable=False)
    descripcion = Column(String(255), nullable=True)
    id_categoria = Column(Integer, ForeignKey("categories.id_categoria"), nullable=False)
    precio = Column(Integer, nullable=False)
    tipo_transaccion = Column(String, nullable=False) 
    usuario_id = Column(Integer, ForeignKey("users.id_usuario"), nullable=False)
    estado = Column(String, nullable=False)
    fecha_publicacion = Column(TIMESTAMP, server_default=func.current_timestamp())
    url_imagen = Column(String(225), nullable=True)
    cantidad = Column(Integer, nullable=False)
    
    

    # Relaciones
    user = relationship("User", back_populates="items", lazy="joined")
 
    shopping_cart = relationship("ShoppingCart", back_populates="articulo")
    transactions = relationship("TransactionHistory", back_populates="item")
    categoria = relationship("Category", back_populates="items")
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

    @property
    def fecha_publicacion_date(self) -> date:
        return self.fecha_publicacion.date() if self.fecha_publicacion else None
