from pydantic import BaseModel, EmailStr
from typing import Optional
from app.utils.security import UserRole
from datetime import datetime
from enum import Enum
class UserRole(str, Enum):
    ADMIN = "ADMIN"
    USER = "USER"

class UserBase(BaseModel):
    nombre: str
    correo_electronico: EmailStr
    telefono: Optional[str] = None
   
    rol: UserRole


class UserCreate(UserBase):
    contrasena: str
    profile_picture_url: Optional[str] = None


class UserUpdate(BaseModel):
    nombre: Optional[str] = None
    correo_electronico: Optional[EmailStr] = None
    telefono: Optional[str] = None

    rol: Optional[UserRole] = None


class UserResponse(BaseModel):
    id_usuario: int
    nombre: str
    correo_electronico: str 
    telefono: Optional[str] = None
    profile_picture_url: Optional[str] = None

    class Config:
        orm_mode = True


# Modelo para verificar usuario
class VerifyUserRequest(BaseModel):
    name: str
    email: EmailStr
class LoginRequest(BaseModel):
    email: str
    password: str