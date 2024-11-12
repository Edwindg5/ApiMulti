from pydantic import BaseModel, EmailStr
from typing import Optional
from app.utils.security import UserRole

class UserBase(BaseModel):
    nombre: str
    correo_electronico: EmailStr
    telefono: Optional[str] = None
    calificacion: Optional[float] = None
    rol: UserRole

class UserCreate(UserBase):
    contrasena: str

class UserResponse(UserBase):
    id_usuario: int
    fecha_registro: str

    class Config:
        orm_mode = True
