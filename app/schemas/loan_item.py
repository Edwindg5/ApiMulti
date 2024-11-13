from pydantic import BaseModel
from typing import Optional
from app.utils.security import TransactionStatus

class LoanItemBase(BaseModel):
    articulo_id: int
    prestador_id: int
    prestatario_id: int
    fecha_devolucion: Optional[str] = None
    estado: TransactionStatus

class LoanItemCreate(LoanItemBase):
    pass


class LoanItemResponse(LoanItemBase):
    id_loan_items: int
    fecha_prestamo: str

    class Config:
        orm_mode = True
