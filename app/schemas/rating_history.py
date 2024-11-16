from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime

class RatingHistoryBase(BaseModel):
    usuario_id: int
    calificador_id: int
    calificacion: float
    comentario: Optional[str] = None

class RatingHistoryCreate(RatingHistoryBase):
    pass

class RatingHistoryResponse(RatingHistoryBase):
    id_rating: int
    fecha_calificacion: str  # Still a string for the response

    class Config:
        orm_mode = True

    # Serialize fecha_calificacion into a string
    @validator("fecha_calificacion", pre=True)
    def serialize_fecha_calificacion(cls, value):
        if isinstance(value, datetime):
            return value.isoformat()  # Convert datetime to ISO 8601 string
        return value
