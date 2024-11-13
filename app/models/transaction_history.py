from sqlalchemy import Column, Integer, Text, TIMESTAMP, ForeignKey, Enum
from app.shared.config.db import Base
from app.utils.security import TransactionStatus
from sqlalchemy.sql import func

class TransactionHistory(Base):
    __tablename__ = "transaction_history"

    id_transaction = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("users.id_usuario"))
    articulo_id = Column(Integer, ForeignKey("items.id_articulo"))
    tipo_transaccion = Column(Enum(TransactionStatus))  # Uso del tipo Enum de SQLAlchemy
    fecha_transaccion = Column(TIMESTAMP, server_default=func.now())
    estado_transaccion = Column(Enum(TransactionStatus))  # Uso del tipo Enum de SQLAlchemy
    detalles = Column(Text)
