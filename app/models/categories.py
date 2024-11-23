# app/models/categories.py
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String
from app.models.items import Item  # Asegúrate de que este import no cause un ciclo
from app.shared.config.db import Base

class Category(Base):
    __tablename__ = 'categories'

    id_categoria = Column(Integer, primary_key=True, autoincrement=True)
    nombre_categoria = Column(String(100), nullable=False)
    descripcion_categoria = Column(String(255), nullable=True)
    items = relationship("Item", back_populates="categoria")