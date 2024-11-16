from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NotificationBase(BaseModel):
    usuario_id: int
    mensaje: str
    leido: Optional[bool] = False

class NotificationCreate(NotificationBase):
    pass

class NotificationResponse(NotificationBase):
    id_notificacion: int  # Cambiado a id_notificacion
    fecha: datetime  # Fecha sigue siendo datetime, pero se serializa automáticamente

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
