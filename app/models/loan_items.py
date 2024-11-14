from sqlalchemy import Column, Integer, TIMESTAMP, Date, Enum, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from app.utils.security import TransactionStatus

Base = declarative_base()

class LoanItem(Base):
    __tablename__ = 'loan_items'

    id_loan_items = Column(Integer, primary_key=True, autoincrement=True)
    articulo_id = Column(Integer, ForeignKey('items.id_articulo'))
    prestador_id = Column(Integer, ForeignKey('users.id_usuario'))
    prestatario_id = Column(Integer, ForeignKey('users.id_usuario'))
    fecha_prestamo = Column(TIMESTAMP, server_default=func.current_timestamp())
    fecha_devolucion = Column(Date, nullable=True)
    estado = Column(Enum(TransactionStatus), nullable=True)
    usuario_id = Column(Integer, ForeignKey('users.id_usuario'))
