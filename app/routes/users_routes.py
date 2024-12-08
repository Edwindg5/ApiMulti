from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from app.models.users import User
from app.schemas.user import UserCreate, UserResponse, UserUpdate, VerifyUserRequest
from app.shared.config.db import get_db
from app.utils.security import hash_password, UserRole
from app.utils.security import verify_password
from app.shared.middlewares.auth_middleware import get_current_user
from app.services.users import (
    create_user,
    get_user_by_id,
    update_user,
    delete_user,
    authenticate_user,
)



def create_admin_user(db: Session):
    admin_email = "admin@example.com"
    admin_password = "admin123"  # Asegúrate de que esto sea seguro en producción
    admin_name = "Admin"

    admin = db.query(User).filter(User.correo_electronico == admin_email).first()
    if not admin:
        hashed_password = hash_password(admin_password)
        admin = User(
            nombre=admin_name,
            correo_electronico=admin_email,
            contrasena=hashed_password,
            rol=UserRole.ADMIN  # Rol de administrador
        )
        db.add(admin)
        db.commit()
        
        
        
def admin_required(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id_usuario == current_user["id"]).first()
    if not user or user.rol != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Acceso denegado")
    return current_user
        
        
from app.utils.security import create_access_token, hash_password, decode_access_token

router = APIRouter(prefix="/users", tags=["users"])



@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = authenticate_user(email, password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    
    access_token = create_access_token(data={"sub": user.correo_electronico})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id_usuario,
            "name": user.nombre,
            "email": user.correo_electronico
        }
    }



# Obtener todos los usuarios con campos específicos
@router.get("/users", tags=["users"])
def get_users(db: Session = Depends(get_db)):
    users = db.query(
        User.id_usuario,  # Asegúrate de incluir id_usuario
        User.nombre,
        User.correo_electronico,
        User.telefono,
        User.fecha_registro.label("fecha_creacion")
    ).filter(User.rol != UserRole.ADMIN).all()

    return {
        "data": [
            {
                "id_usuario": user.id_usuario,
                "nombre": user.nombre,
                "correo_electronico": user.correo_electronico,
                "telefono": user.telefono,
                "fecha_creacion": user.fecha_creacion,
            }
            for user in users
        ]
    }



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
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id_usuario,
            "name": user.nombre,
            "email": user.correo_electronico
        }
    }





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
       
        rol=user.rol,
        contrasena=hashed_password,
        profile_picture_url=user.profile_picture_url,  # Guardar la URL de la imagen
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
    user = db.query(User).filter(User.id_usuario == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(user)
    db.commit()
    return {"message": "Usuario eliminado correctamente"}

