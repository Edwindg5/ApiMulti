from sqlalchemy import Column, Integer, TIMESTAMP, DATE, ForeignKey
from app.shared.config.db import Base
from app.utils.security import TransactionStatus
from sqlalchemy.sql import func

class LoanItem(Base):
    __tablename__ = "loan_items"

    id_loan_items = Column(Integer, primary_key=True, index=True)
    articulo_id = Column(Integer, ForeignKey("items.id_articulo"))
    prestador_id = Column(Integer, ForeignKey("users.id_usuario"))
    prestatario_id = Column(Integer, ForeignKey("users.id_usuario"))
    fecha_prestamo = Column(TIMESTAMP, server_default=func.now())
    fecha_devolucion = Column(DATE)
    estado = Column(TransactionStatus)
