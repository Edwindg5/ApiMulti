from typing import Optional
from pydantic import BaseModel

class NotificationBase(BaseModel):
    usuario_id: int
    mensaje: str
    leido: Optional[bool] = False

class NotificationCreate(NotificationBase):
    pass

class NotificationResponse(NotificationBase):
    id_notificacion: int
    fecha: str

    class Config:
        orm_mode = True
