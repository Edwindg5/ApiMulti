from sqlalchemy import Column, Integer, Text, TIMESTAMP, Enum, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from app.utils.security import TransactionStatus

Base = declarative_base()

class TransactionHistory(Base):
    __tablename__ = 'transaction_history'

    id_transaction = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey('users.id_usuario'))
    articulo_id = Column(Integer, ForeignKey('items.id_articulo'))
    tipo_transaccion = Column(Enum(TransactionStatus), nullable=True)
    fecha_transaccion = Column(TIMESTAMP, server_default=func.current_timestamp())
    estado_transaccion = Column(Enum(TransactionStatus), nullable=True)
    detalles = Column(Text, nullable=True)
