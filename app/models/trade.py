from sqlalchemy import Column, Integer, String, ForeignKey, Enum, TIMESTAMP
from app.shared.config.db import Base
from app.utils.security import TransactionStatus
from sqlalchemy.sql import func

class Trade(Base):
    __tablename__ = "trades"

    id_trade = Column(Integer, primary_key=True, index=True)
    trade_name = Column(String(100), nullable=False)
    estado = Column(Enum(TransactionStatus))  # Corregido para usar Enum con el enum TransactionStatus
    user_id = Column(Integer, ForeignKey("users.id_usuario"))
    created_at = Column(TIMESTAMP, server_default=func.now())
