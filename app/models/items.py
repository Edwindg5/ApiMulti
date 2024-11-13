from sqlalchemy import Column, Integer, String, Text, ForeignKey, DECIMAL, TIMESTAMP, Enum
from app.shared.config.db import Base
from app.utils.security import TransactionStatus
from sqlalchemy.sql import func

class Item(Base):
    __tablename__ = "items"

    id_articulo = Column(Integer, primary_key=True, index=True)
    nombre_articulo = Column(String(100), nullable=False)
    descripcion = Column(Text)
    categoria_id = Column(Integer, ForeignKey("categories.id_categoria"))
    precio = Column(DECIMAL(10, 2))
    tipo_transaccion = Column(Enum(TransactionStatus))
    usuario_id = Column(Integer, ForeignKey("users.id_usuario"))
    estado = Column(Enum(TransactionStatus))
    fecha_publicacion = Column(TIMESTAMP, server_default=func.now())
