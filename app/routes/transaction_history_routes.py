from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.transaction_history import TransactionHistoryCreate, TransactionHistoryResponse
from app.models.transaction_history import TransactionHistory
from app.shared.config.db import get_db

router = APIRouter()

@router.post("/", response_model=TransactionHistoryResponse)
def create_transaction_history(transaction: TransactionHistoryCreate, db: Session = Depends(get_db)):
    db_transaction = TransactionHistory(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@router.get("/{transaction_id}", response_model=TransactionHistoryResponse)
def read_transaction_history(transaction_id: int, db: Session = Depends(get_db)):
    transaction = db.query(TransactionHistory).filter(TransactionHistory.id_transaction == transaction_id).first()
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction history not found")
    return transaction

@router.put("/{transaction_id}", response_model=TransactionHistoryResponse)
def update_transaction_history(transaction_id: int, transaction: TransactionHistoryCreate, db: Session = Depends(get_db)):
    db_transaction = db.query(TransactionHistory).filter(TransactionHistory.id_transaction == transaction_id).first()
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction history not found")
    for key, value in transaction.dict().items():
        setattr(db_transaction, key, value)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@router.delete("/{transaction_id}")
def delete_transaction_history(transaction_id: int, db: Session = Depends(get_db)):
    db_transaction = db.query(TransactionHistory).filter(TransactionHistory.id_transaction == transaction_id).first()
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction history not found")
    db.delete(db_transaction)
    db.commit()
    return {"message": "Transaction history deleted successfully"}
