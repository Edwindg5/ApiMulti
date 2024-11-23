from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.shared.config.db import Base

class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, autoincrement=True)
    file_url = Column(String, nullable=False)  # URL del archivo en S3
    original_name = Column(String, nullable=True)  # Nombre original del archivo
    uploaded_at = Column(TIMESTAMP, server_default=func.current_timestamp())  # Fecha de subida
    user_id = Column(Integer, ForeignKey("users.id_usuario"), nullable=True)  # Usuario que subió la imagen

    # Relación con el modelo User (si es necesario)
    user = relationship("User", back_populates="images")  # Asegúrate de definir `images` en el modelo User
