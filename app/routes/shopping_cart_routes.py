from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from app.schemas.shopping_cart import ShoppingCartCreate, ShoppingCartResponse
from app.models.shopping_cart import ShoppingCart
from app.shared.config.db import get_db

router = APIRouter()

@router.post("/", response_model=ShoppingCartResponse)
def create_shopping_cart(cart_item: ShoppingCartCreate, db: Session = Depends(get_db)):
    db_cart_item = ShoppingCart(**cart_item.dict())
    db.add(db_cart_item)
    db.commit()
    db.refresh(db_cart_item)
    return jsonable_encoder(db_cart_item)

@router.get("/{cart_item_id}", response_model=ShoppingCartResponse)
def read_shopping_cart(cart_item_id: int, db: Session = Depends(get_db)):
    cart_item = db.query(ShoppingCart).filter(ShoppingCart.id_shopping_cart == cart_item_id).first()
    if cart_item is None:
        raise HTTPException(status_code=404, detail="Shopping cart item not found")
    return jsonable_encoder(cart_item)

@router.put("/{cart_item_id}", response_model=ShoppingCartResponse)
def update_shopping_cart(cart_item_id: int, cart_item: ShoppingCartCreate, db: Session = Depends(get_db)):
    db_cart_item = db.query(ShoppingCart).filter(ShoppingCart.id_shopping_cart == cart_item_id).first()
    if db_cart_item is None:
        raise HTTPException(status_code=404, detail="Shopping cart item not found")
    for key, value in cart_item.dict().items():
        setattr(db_cart_item, key, value)
    db.commit()
    db.refresh(db_cart_item)
    return jsonable_encoder(db_cart_item)

@router.delete("/{cart_item_id}")
def delete_shopping_cart(cart_item_id: int, db: Session = Depends(get_db)):
    db_cart_item = db.query(ShoppingCart).filter(ShoppingCart.id_shopping_cart == cart_item_id).first()
    if db_cart_item is None:
        raise HTTPException(status_code=404, detail="Shopping cart item not found")
    db.delete(db_cart_item)
    db.commit()
    return {"message": "Shopping cart item deleted successfully"}
