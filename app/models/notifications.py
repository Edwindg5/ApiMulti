from sqlalchemy import Column, Integer, Text, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Notification(Base):
    __tablename__ = 'notifications'

    id_notificacion = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey('users.id_usuario'))
    mensaje = Column(Text, nullable=True)
    leido = Column(Boolean, default=False)
    fecha = Column(TIMESTAMP, server_default=func.current_timestamp())
