# app/models/user.py

from sqlalchemy import Column, Integer, String, Enum
from app.shared.config.db import Base
from app.utils.security import UserRole

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    rol = Column(Enum(UserRole), nullable=False)  # Usamos Enum de SQLAlchemy
