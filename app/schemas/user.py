from pydantic import BaseModel, EmailStr
from typing import Optional
from app.utils.security import UserRole
from datetime import datetime

class UserBase(BaseModel):
    nombre: str
    correo_electronico: EmailStr
    telefono: Optional[str] = None
    calificacion: Optional[float] = None
    rol: UserRole

class UserCreate(UserBase):
    contrasena: str

class UserUpdate(BaseModel):
    nombre: Optional[str] = None
    correo_electronico: Optional[EmailStr] = None
    telefono: Optional[str] = None
    calificacion: Optional[float] = None
    rol: Optional[UserRole] = None

class UserResponse(UserBase):
    id_usuario: int
    fecha_registro: datetime

    class Config:
        orm_mode = True
