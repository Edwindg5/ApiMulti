from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from app.models.users import User
from app.schemas.user import UserCreate, UserUpdate

def get_user_by_correo_electronico(correo: str, db: Session):
    return db.query(User).filter(User.correo_electronico == correo).first()

def create_user(user_data: UserCreate, db: Session):
    existing_user = get_user_by_correo_electronico(user_data.correo_electronico, db)
    if existing_user:
        raise HTTPException(status_code=400, detail="Correo electrónico ya registrado.")
    
    new_user = User(**user_data.dict())
    db.add(new_user)
    try:
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error al guardar el usuario en la base de datos.")

def get_user_by_id(user_id: int, db: Session):
    user = db.query(User).filter(User.id_usuario == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    return user

def update_user(user_id: int, user_data: UserUpdate, db: Session):
    db_user = get_user_by_id(user_id, db)
    for key, value in user_data.dict(exclude_unset=True).items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(user_id: int, db: Session):
    db_user = get_user_by_id(user_id, db)
    db.delete(db_user)
    db.commit()
    return {"message": "Usuario eliminado correctamente"}
