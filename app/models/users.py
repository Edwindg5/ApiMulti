from sqlalchemy import Column, Integer, String, DECIMAL, TIMESTAMP, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.shared.config.db import Base
from app.utils.security import UserRole

class User(Base):
    __tablename__ = 'users'

    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    correo_electronico = Column(String(100), unique=True, nullable=False)
    contrasena = Column(String(255), nullable=False)  # Debe contener el hash de la contraseña
    telefono = Column(String(15), nullable=True)
    calificacion = Column(DECIMAL(3, 2), nullable=True)
    fecha_registro = Column(TIMESTAMP, server_default=func.current_timestamp())
    rol = Column(Enum(UserRole), nullable=False)

    # Relación con el modelo Item
    items = relationship("Item", back_populates="user")
