from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.loan_item import LoanItemsCreate, LoanItemsResponse
from app.models.loan_item import LoanItems
from app.shared.config.db import get_db

router = APIRouter()

@router.post("/", response_model=LoanItemsResponse)
def create_loan_item(loan_item: LoanItemsCreate, db: Session = Depends(get_db)):
    db_loan_item = LoanItems(**loan_item.dict())
    db.add(db_loan_item)
    db.commit()
    db.refresh(db_loan_item)
    return db_loan_item

@router.get("/{loan_item_id}", response_model=LoanItemsResponse)
def read_loan_item(loan_item_id: int, db: Session = Depends(get_db)):
    loan_item = db.query(LoanItems).filter(LoanItems.id_loan_items == loan_item_id).first()
    if loan_item is None:
        raise HTTPException(status_code=404, detail="Loan item not found")
    return loan_item

@router.put("/{loan_item_id}", response_model=LoanItemsResponse)
def update_loan_item(loan_item_id: int, loan_item: LoanItemsCreate, db: Session = Depends(get_db)):
    db_loan_item = db.query(LoanItems).filter(LoanItems.id_loan_items == loan_item_id).first()
    if db_loan_item is None:
        raise HTTPException(status_code=404, detail="Loan item not found")
    for key, value in loan_item.dict().items():
        setattr(db_loan_item, key, value)
    db.commit()
    db.refresh(db_loan_item)
    return db_loan_item

@router.delete("/{loan_item_id}")
def delete_loan_item(loan_item_id: int, db: Session = Depends(get_db)):
    db_loan_item = db.query(LoanItems).filter(LoanItems.id_loan_items == loan_item_id).first()
    if db_loan_item is None:
        raise HTTPException(status_code=404, detail="Loan item not found")
    db.delete(db_loan_item)
    db.commit()
    return {"message": "Loan item deleted successfully"}
