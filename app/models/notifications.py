from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.shared.config.db import Base

class Notification(Base):
    __tablename__ = "notifications"

    id_notificacion = Column(Integer, primary_key=True, index=True)  # Ajustado para coincidir con la base de datos
    usuario_id = Column(Integer, ForeignKey("users.id_usuario"), nullable=False)
    mensaje = Column(String, nullable=False)
    leido = Column(Boolean, default=False)
    fecha = Column(DateTime, default=datetime.utcnow)

    # Relación con el modelo User
    user = relationship("User", back_populates="notifications")
    
