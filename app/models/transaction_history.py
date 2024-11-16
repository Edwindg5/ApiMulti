from sqlalchemy import Column, Integer, Text, TIMESTAMP, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.shared.config.db import Base
from app.utils.security import TransactionStatus, TransactionType

class TransactionHistory(Base):
    __tablename__ = "transaction_history"

    id_transaction = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("users.id_usuario"), nullable=False)
    articulo_id = Column(Integer, ForeignKey("items.id_articulo"), nullable=False)
    tipo_transaccion = Column(Enum(TransactionType), nullable=False)
    estado_transaccion = Column(Enum(TransactionStatus), nullable=False, default=TransactionStatus.DISPONIBLE)
    detalles = Column(Text, nullable=True)
    fecha_transaccion = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="transactions")
    item = relationship("Item", back_populates="transactions")
