from sqlalchemy import Column, Integer, Text, DECIMAL, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class RatingHistory(Base):
    __tablename__ = 'rating_history'

    id_rating = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey('users.id_usuario'))
    calificador_id = Column(Integer, ForeignKey('users.id_usuario'))
    calificacion = Column(DECIMAL(3, 2), nullable=True)
    comentario = Column(Text, nullable=True)
    fecha_calificacion = Column(TIMESTAMP, server_default=func.current_timestamp())
