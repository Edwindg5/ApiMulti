from sqlalchemy import Column, Integer, TIMESTAMP, Enum, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from app.utils.security import TransactionStatus

Base = declarative_base()

class Trade(Base):
    __tablename__ = 'trades'

    id_trade = Column(Integer, primary_key=True, autoincrement=True)
    articulo_solicitado_id = Column(Integer, ForeignKey('items.id_articulo'))
    articulo_ofrecido_id = Column(Integer, ForeignKey('items.id_articulo'))
    usuario_solicitante_id = Column(Integer, ForeignKey('users.id_usuario'))
    usuario_ofertador_id = Column(Integer, ForeignKey('users.id_usuario'))
    fecha_oferta = Column(TIMESTAMP, server_default=func.current_timestamp())
    estado = Column(Enum(TransactionStatus), nullable=True)
    usuario_id = Column(Integer, ForeignKey('users.id_usuario'))
