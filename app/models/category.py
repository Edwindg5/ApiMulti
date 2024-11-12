from sqlalchemy import Column, Integer, String
from app.shared.config.db import Base

class Category(Base):
    __tablename__ = "categories"

    id_categoria = Column(Integer, primary_key=True, index=True)
    nombre_categoria = Column(String(100), nullable=False)
    descripcion_categoria = Column(String(255))
