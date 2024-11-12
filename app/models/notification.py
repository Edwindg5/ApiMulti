from sqlalchemy import Column, Integer, Text, TIMESTAMP, Boolean, ForeignKey
from app.shared.config.db import Base
from sqlalchemy.sql import func

class Notification(Base):
    __tablename__ = "notifications"

    id_notificacion = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("users.id_usuario"))
    mensaje = Column(Text, nullable=False)
    leido = Column(Boolean, default=False)
    fecha = Column(TIMESTAMP, server_default=func.now())
