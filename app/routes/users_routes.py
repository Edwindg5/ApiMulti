from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.shared.config.db import get_db
from app.services.users import (
    create_user,
    get_user_by_id,
    update_user,
    delete_user,
)

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse)
def create_user_route(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(user, db)

@router.get("/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    return get_user_by_id(user_id, db)

@router.put("/{user_id}", response_model=UserResponse)
def update_user_route(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    return update_user(user_id, user, db)

@router.delete("/{user_id}")
def delete_user_route(user_id: int, db: Session = Depends(get_db)):
    return delete_user(user_id, db)
