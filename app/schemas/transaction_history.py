from pydantic import BaseModel
from typing import Optional
from app.utils.security import TransactionStatus

class TransactionHistoryBase(BaseModel):
    usuario_id: int
    articulo_id: int
    tipo_transaccion: TransactionStatus
    detalles: Optional[str] = None

class TransactionHistoryCreate(TransactionHistoryBase):
    pass

class TransactionHistoryResponse(TransactionHistoryBase):
    id_transaction: int
    fecha_transaccion: str
    estado_transaccion: TransactionStatus

    class Config:
        orm_mode = True
