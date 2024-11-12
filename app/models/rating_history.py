from sqlalchemy import Column, Integer, Text, TIMESTAMP, DECIMAL, ForeignKey
from app.shared.config.db import Base
from sqlalchemy.sql import func

class RatingHistory(Base):
    __tablename__ = "rating_history"

    id_rating = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("users.id_usuario"))
    calificador_id = Column(Integer, ForeignKey("users.id_usuario"))
    calificacion = Column(DECIMAL(3, 2))
    comentario = Column(Text)
    fecha_calificacion = Column(TIMESTAMP, server_default=func.now())
