from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.trade import TradeCreate, TradeResponse
from app.models.trades import Trade
from app.shared.config.db import get_db
from app.models.notifications import Notification

router = APIRouter()

@router.post("/", response_model=TradeResponse)
def create_trade(trade: TradeCreate, db: Session = Depends(get_db)):
    db_trade = Trade(**trade.dict())
    db.add(db_trade)
    db.commit()
    db.refresh(db_trade)
    # Convertir fecha_oferta a string antes de devolver
    db_trade.fecha_oferta = db_trade.fecha_oferta.isoformat()
    return db_trade




@router.post("/exchange_with_notification", response_model=TradeResponse)
def request_exchange_with_notification(trade: TradeCreate, db: Session = Depends(get_db)):
    # Crear intercambio
    db_trade = Trade(**trade.dict())
    db.add(db_trade)
    db.commit()
    db.refresh(db_trade)

    # Crear notificación
    notification_data = {
        "usuario_id": trade.owner_id,
        "mensaje": f"Te han solicitado un intercambio para {trade.description}",
    }
    db_notification = Notification(**notification_data)
    db.add(db_notification)
    db.commit()

    return db_trade


@router.get("/{trade_id}", response_model=TradeResponse)
def read_trade(trade_id: int, db: Session = Depends(get_db)):
    trade = db.query(Trade).filter(Trade.id_trade == trade_id).first()
    if trade is None:
        raise HTTPException(status_code=404, detail="Trade not found")
    return trade

@router.put("/{trade_id}", response_model=TradeResponse)
def update_trade(trade_id: int, trade: TradeCreate, db: Session = Depends(get_db)):
    db_trade = db.query(Trade).filter(Trade.id_trade == trade_id).first()
    if db_trade is None:
        raise HTTPException(status_code=404, detail="Trade not found")
    for key, value in trade.dict().items():
        setattr(db_trade, key, value)
    db.commit()
    db.refresh(db_trade)
    return db_trade
@router.put("/{trade_id}/accept", response_model=TradeResponse)
def accept_trade(trade_id: int, db: Session = Depends(get_db)):
    db_trade = db.query(Trade).filter(Trade.id_trade == trade_id).first()
    if db_trade is None:
        raise HTTPException(status_code=404, detail="Trade not found")
    db_trade.status = "accepted"  # Cambiar el estado del intercambio
    db.commit()
    db.refresh(db_trade)
    return db_trade
@router.put("/{trade_id}/reject", response_model=TradeResponse)
def reject_trade(trade_id: int, db: Session = Depends(get_db)):
    db_trade = db.query(Trade).filter(Trade.id_trade == trade_id).first()
    if db_trade is None:
        raise HTTPException(status_code=404, detail="Trade not found")
    db_trade.status = "rejected"  # Cambiar el estado del intercambio
    db.commit()
    db.refresh(db_trade)
    return db_trade


@router.delete("/{trade_id}")
def delete_trade(trade_id: int, db: Session = Depends(get_db)):
    db_trade = db.query(Trade).filter(Trade.id_trade == trade_id).first()
    if db_trade is None:
        raise HTTPException(status_code=404, detail="Trade not found")
    db.delete(db_trade)
    db.commit()
    return {"message": "Trade deleted successfully"}
