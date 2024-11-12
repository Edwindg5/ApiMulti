from pydantic import BaseModel
from typing import Optional

class RatingHistoryBase(BaseModel):
    usuario_id: int
    calificador_id: int
    calificacion: float
    comentario: Optional[str] = None

class RatingHistoryCreate(RatingHistoryBase):
    pass

class RatingHistoryResponse(RatingHistoryBase):
    id_rating: int
    fecha_calificacion: str

    class Config:
        orm_mode = True
