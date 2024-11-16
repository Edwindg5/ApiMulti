from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.transaction_history import TransactionHistoryCreate, TransactionHistoryResponse
from app.models.transaction_history import TransactionHistory
from app.shared.config.db import get_db
from app.utils.security import TransactionStatus

router = APIRouter()

@router.post("/", response_model=TransactionHistoryResponse)
def create_transaction_history(transaction: TransactionHistoryCreate, db: Session = Depends(get_db)):
    estado_transaccion = transaction.estado_transaccion or TransactionStatus.DISPONIBLE

    db_transaction = TransactionHistory(
        usuario_id=transaction.usuario_id,
        articulo_id=transaction.articulo_id,
        tipo_transaccion=transaction.tipo_transaccion,
        estado_transaccion=estado_transaccion,
        detalles=transaction.detalles
    )

    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return TransactionHistoryResponse.from_orm(db_transaction)

@router.get("/{transaction_id}", response_model=TransactionHistoryResponse)
def read_transaction_history(transaction_id: int, db: Session = Depends(get_db)):
    transaction = db.query(TransactionHistory).filter(TransactionHistory.id_transaction == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction history not found")
    return TransactionHistoryResponse.from_orm(transaction)

@router.put("/{transaction_id}", response_model=TransactionHistoryResponse)
def update_transaction_history(transaction_id: int, transaction: TransactionHistoryCreate, db: Session = Depends(get_db)):
    db_transaction = db.query(TransactionHistory).filter(TransactionHistory.id_transaction == transaction_id).first()
    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transaction history not found")
    for key, value in transaction.dict(exclude_unset=True).items():
        setattr(db_transaction, key, value)
    db.commit()
    db.refresh(db_transaction)
    return TransactionHistoryResponse.from_orm(db_transaction)

@router.delete("/{transaction_id}")
def delete_transaction_history(transaction_id: int, db: Session = Depends(get_db)):
    db_transaction = db.query(TransactionHistory).filter(TransactionHistory.id_transaction == transaction_id).first()
    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transaction history not found")
    db.delete(db_transaction)
    db.commit()
    return {"detail": "Transaction deleted successfully"}
