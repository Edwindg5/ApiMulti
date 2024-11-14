from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP,func
from sqlalchemy.orm import relationship
from app.shared.config.db import Base


class Item(Base):
    __tablename__ = 'items'

    id_articulo = Column(Integer, primary_key=True, autoincrement=True)
    nombre_articulo = Column(String(100), nullable=False)
    descripcion = Column(String(255), nullable=True)
    categoria_id = Column(Integer, nullable=False)
    precio = Column(Integer, nullable=False)
    tipo_transaccion = Column(String(50), nullable=False)  # O usa Enum si es un valor fijo
    usuario_id = Column(Integer, ForeignKey("users.id_usuario"), nullable=False)
    estado = Column(String(50), nullable=False)
    fecha_publicacion = Column(TIMESTAMP, server_default=func.current_timestamp())

    # Relación con el modelo User
    user = relationship("User", back_populates="items")
