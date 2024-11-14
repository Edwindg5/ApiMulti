from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.loan_item import LoanItemCreate, LoanItemResponse
from app.models.loan_items import LoanItem
from app.shared.config.db import get_db

router = APIRouter()

@router.post("/", response_model=LoanItemResponse)
def create_loan_item(loan_item: LoanItemCreate, db: Session = Depends(get_db)):
    db_loan_item = LoanItem(**loan_item.dict())
    db.add(db_loan_item)
    db.commit()
    db.refresh(db_loan_item)
    return db_loan_item

@router.get("/{loan_item_id}", response_model=LoanItemResponse)
def read_loan_item(loan_item_id: int, db: Session = Depends(get_db)):
    loan_item = db.query(LoanItem).filter(LoanItem.id_loan_items == loan_item_id).first()
    if loan_item is None:
        raise HTTPException(status_code=404, detail="Loan item not found")
    return loan_item

@router.put("/{loan_item_id}", response_model=LoanItemResponse)
def update_loan_item(loan_item_id: int, loan_item: LoanItemCreate, db: Session = Depends(get_db)):
    db_loan_item = db.query(LoanItem).filter(LoanItem.id_loan_items == loan_item_id).first()
    if db_loan_item is None:
        raise HTTPException(status_code=404, detail="Loan item not found")
    for key, value in loan_item.dict().items():
        setattr(db_loan_item, key, value)
    db.commit()
    db.refresh(db_loan_item)
    return db_loan_item

@router.delete("/{loan_item_id}")
def delete_loan_item(loan_item_id: int, db: Session = Depends(get_db)):
    db_loan_item = db.query(LoanItem).filter(LoanItem.id_loan_items == loan_item_id).first()
    if db_loan_item is None:
        raise HTTPException(status_code=404, detail="Loan item not found")
    db.delete(db_loan_item)
    db.commit()
    return {"message": "Loan item deleted successfully"}
