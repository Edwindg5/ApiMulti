from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from app.models.users import User
from app.schemas.user import UserCreate, UserResponse, UserUpdate, VerifyUserRequest
from app.shared.config.db import get_db
from app.services.users import (
    create_user,
    get_user_by_id,
    update_user,
    delete_user,
    authenticate_user,
)
from app.utils.security import create_access_token, hash_password, decode_access_token

router = APIRouter(prefix="/users", tags=["users"])


# Endpoint para verificar usuario con ilike
@router.post("/verify")
def verify_user(request: VerifyUserRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(
        User.nombre.ilike(request.name.strip()),
        User.correo_electronico.ilike(request.email.strip())
    ).first()
    if user:
        return {"exists": True, "userId": user.id_usuario}
    return {"exists": False}


# Endpoint de login
@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = authenticate_user(email, password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    access_token = create_access_token(data={"sub": user.correo_electronico})
    return {"access_token": access_token, "token_type": "bearer"}


# Crear usuario
@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.correo_electronico == user.correo_electronico).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")
    
    hashed_password = hash_password(user.contrasena)
    
    new_user = User(
        nombre=user.nombre,
        correo_electronico=user.correo_electronico,
        telefono=user.telefono,
        calificacion=user.calificacion,
        rol=user.rol,
        contrasena=hashed_password,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


# Obtener un usuario por ID
@router.get("/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(user_id, db)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    return user


# Actualizar un usuario
@router.put("/{user_id}", response_model=UserResponse)
def update_user_route(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    updated_user = update_user(user_id, user, db)
    return updated_user


# Eliminar un usuario
@router.delete("/{user_id}")
def delete_user_route(user_id: int, db: Session = Depends(get_db)):
    delete_user(user_id, db)
    return {"message": "Usuario eliminado correctamente"}
