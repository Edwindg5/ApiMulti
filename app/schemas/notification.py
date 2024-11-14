from pydantic import BaseModel
from typing import Optional

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
