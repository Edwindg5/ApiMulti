from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from app.shared.config.db import Base

class Image(Base):
    __tablename__ = "images"

    id_imagen = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(255), nullable=False)
    item_id = Column(Integer, ForeignKey("items.id_articulo"), nullable=False)

    # Relación inversa con el modelo Item
    item = relationship("Item", back_populates="images")
