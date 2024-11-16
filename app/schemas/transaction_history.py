from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional
from app.utils.security import TransactionStatus, TransactionType

class TransactionHistoryBase(BaseModel):
    usuario_id: int
    articulo_id: int
    tipo_transaccion: TransactionType
    estado_transaccion: Optional[TransactionStatus] = None
    detalles: Optional[str] = None

class TransactionHistoryCreate(TransactionHistoryBase):
    pass

class TransactionHistoryResponse(TransactionHistoryBase):
    id_transaction: int
    fecha_transaccion: str

    @validator("fecha_transaccion", pre=True)
    def format_fecha_transaccion(cls, value):
        if isinstance(value, datetime):
            return value.isoformat()  # Formatea como string ISO 8601
        return value

    class Config:
        from_attributes = True  # Pydantic v2: Permitir from_orm
