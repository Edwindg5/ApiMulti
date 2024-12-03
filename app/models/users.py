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
    fecha_registro = Column(TIMESTAMP, server_default=func.current_timestamp())
    rol = Column(Enum(UserRole), nullable=False)
    profile_picture_url = Column(String(255), nullable=True) 

    # Relaciones
    items = relationship("Item", back_populates="user")
    shopping_cart = relationship("ShoppingCart", back_populates="user")
    transactions = relationship("TransactionHistory", back_populates="user")
    notifications = relationship("Notification", back_populates="user")
    
    ratings = relationship(
        "RatingHistory",
        foreign_keys="RatingHistory.usuario_id",
        back_populates="user"
    )
    given_ratings = relationship(
        "RatingHistory",
        foreign_keys="RatingHistory.calificador_id",
        back_populates="calificador"
    )
