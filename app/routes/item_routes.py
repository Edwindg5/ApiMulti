from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.items import Item
from app.schemas.items import ItemCreate, ItemResponse
from app.shared.config.db import get_db

router = APIRouter()

@router.post("/", response_model=ItemResponse)
def crear_item(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/{item_id}", response_model=ItemResponse)
def leer_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id_articulo == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.delete("/{item_id}")
def eliminar_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id_articulo == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    try:
        db.delete(item)
        db.commit()
        return {"message": "Item deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting item: {str(e)}")
