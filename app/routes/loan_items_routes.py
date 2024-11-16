from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.loan_item import LoanItemCreate, LoanItemResponse
from app.models.loan_items import LoanItem
from app.shared.config.db import get_db

router = APIRouter(prefix="/loan-items", tags=["Loan Items"])

@router.post("/", response_model=LoanItemResponse)
def create_loan_item(loan_item: LoanItemCreate, db: Session = Depends(get_db)):
    try:
        db_loan_item = LoanItem(**loan_item.dict())
        db.add(db_loan_item)
        db.commit()
        db.refresh(db_loan_item)
        return db_loan_item
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating loan item: {str(e)}")

@router.get("/{id_loan_items}", response_model=LoanItemResponse)
def get_loan_item(id_loan_items: int, db: Session = Depends(get_db)):
    loan_item = db.query(LoanItem).filter(LoanItem.id_loan_items == id_loan_items).first()
    if not loan_item:
        raise HTTPException(status_code=404, detail="Loan item not found")
    return loan_item

@router.put("/{id_loan_items}", response_model=LoanItemResponse)
def update_loan_item(id_loan_items: int, loan_item: LoanItemCreate, db: Session = Depends(get_db)):
    try:
        db_loan_item = db.query(LoanItem).filter(LoanItem.id_loan_items == id_loan_items).first()
        if not db_loan_item:
            raise HTTPException(status_code=404, detail="Loan item not found")
        for key, value in loan_item.dict().items():
            setattr(db_loan_item, key, value)
        db.commit()
        db.refresh(db_loan_item)
        return db_loan_item
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating loan item: {str(e)}")
@router.delete("/{id_loan_items}")
def delete_loan_item(id_loan_items: int, db: Session = Depends(get_db)):
    try:
        db_loan_item = db.query(LoanItem).filter(LoanItem.id_loan_items == id_loan_items).first()
        if not db_loan_item:
            raise HTTPException(status_code=404, detail="Loan item not found")
        db.delete(db_loan_item)
        db.commit()
        return {"message": "Loan item deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting loan item: {str(e)}")
