from sqlalchemy import Column, Integer, String, DECIMAL, TIMESTAMP
from sqlalchemy.sql import func
from app.shared.config.db import Base
from app.utils.security import UserRole

class User(Base):
    __tablename__ = "users"

    id_usuario = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    correo_electronico = Column(String(100), unique=True, nullable=False)
    contrasena = Column(String(255), nullable=False)
    telefono = Column(String(15))
    calificacion = Column(DECIMAL(3, 2))
    fecha_registro = Column(TIMESTAMP, server_default=func.now())
    rol = Column(UserRole, nullable=False)
