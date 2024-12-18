from pydantic import BaseModel, validator
from datetime import datetime
from app.utils.security import TransactionStatus

class TradeBase(BaseModel):
    articulo_solicitado_id: int
    articulo_ofrecido_id: int
    usuario_solicitante_id: int
    usuario_ofertador_id: int
    estado: TransactionStatus

class TradeCreate(TradeBase):
    pass

class TradeResponse(TradeBase):
    id_trade: int
    fecha_oferta: str

    class Config:
        orm_mode = True

    @validator("fecha_oferta", pre=True, always=True)
    def format_fecha_oferta(cls, value):
        if isinstance(value, datetime):
            return value.isoformat()  # Convierte a formato ISO 8601
        return value
