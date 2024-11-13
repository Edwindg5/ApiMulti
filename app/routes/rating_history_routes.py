from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.rating_history import RatingHistoryCreate, RatingHistoryResponse
from app.models.rating_history import RatingHistory
from app.shared.config.db import get_db

router = APIRouter()

@router.post("/", response_model=RatingHistoryResponse)
def create_rating_history(rating: RatingHistoryCreate, db: Session = Depends(get_db)):
    
    db_rating = RatingHistory(**rating.dict())
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    return db_rating

@router.get("/{rating_id}", response_model=RatingHistoryResponse)
def read_rating_history(rating_id: int, db: Session = Depends(get_db)):
    rating = db.query(RatingHistory).filter(RatingHistory.id_rating == rating_id).first()
    if rating is None:
        raise HTTPException(status_code=404, detail="Rating history not found")
    return rating

@router.put("/{rating_id}", response_model=RatingHistoryResponse)
def update_rating_history(rating_id: int, rating: RatingHistoryCreate, db: Session = Depends(get_db)):
    db_rating = db.query(RatingHistory).filter(RatingHistory.id_rating == rating_id).first()
    if db_rating is None:
        raise HTTPException(status_code=404, detail="Rating history not found")
    for key, value in rating.dict().items():
        setattr(db_rating, key, value)
    db.commit()
    db.refresh(db_rating)
    return db_rating

@router.delete("/{rating_id}")
def delete_rating_history(rating_id: int, db: Session = Depends(get_db)):
    db_rating = db.query(RatingHistory).filter(RatingHistory.id_rating == rating_id).first()
    if db_rating is None:
        raise HTTPException(status_code=404, detail="Rating history not found")
    db.delete(db_rating)
    db.commit()
    return {"message": "Rating history deleted successfully"}
