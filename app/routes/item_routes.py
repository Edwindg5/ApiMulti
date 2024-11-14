from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.items import Item
from app.schemas.items import ItemCreate, ItemResponse
from app.shared.config.db import get_db

router = APIRouter()

@router.post("/", response_model=ItemResponse)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/{item_id}", response_model=ItemResponse)
def read_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id_articulo == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
