from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.trade import TradeCreate, TradeResponse, TradeBase
from app.models.trades import Trade
from app.shared.config.db import get_db
from app.models.notifications import Notification
from typing import List
from app.models.users import User
from app.schemas.user import UserResponse
from app.models.items import Item




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
@router.get("/user/{user_id}/trades")
async def get_trades_by_user(user_id: int, db: Session = Depends(get_db)):
    # Verificar si el usuario existe
    user = db.query(User).filter(User.id_usuario == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Obtener todas las transacciones (trades) donde el usuario sea solicitante
    trades = db.query(Trade).filter(Trade.usuario_solicitante_id == user_id).all()

    if not trades:
        raise HTTPException(status_code=404, detail="No trades found for this user")

    # Construir la respuesta
    trade_details = []
    for trade in trades:
        # Obtener los artículos asociados
        articulo_solicitado = db.query(Item).filter(Item.id_articulo == trade.articulo_solicitado_id).first()
        articulo_ofrecido = db.query(Item).filter(Item.id_articulo == trade.articulo_ofrecido_id).first()

        # Obtener el usuario ofertante
        usuario_solicitante = db.query(User).filter(User.id_usuario == trade.usuario_ofertador_id).first()

        # Formatear cada transacción
        trade_details.append({
            "trade": {
                "id_trade": trade.id_trade,
                "estado": trade.estado,
                "fecha_oferta": trade.fecha_oferta
            },
            "usuario_solicitante": {
                "id": usuario_solicitante.id_usuario,
                "nombre": usuario_solicitante.nombre,
                "email": usuario_solicitante.correo_electronico
            },
            "articulo_solicitado": {
                "id": articulo_solicitado.id_articulo,
                "nombre": articulo_solicitado.nombre_articulo,
                "descripcion": articulo_solicitado.descripcion,
                "imagen": articulo_solicitado.url_imagen,
                "estado": articulo_solicitado.estado
            },
            "articulo_ofrecido": {
                "id": articulo_ofrecido.id_articulo,
                "nombre": articulo_ofrecido.nombre_articulo,
                "descripcion": articulo_ofrecido.descripcion,
                "imagen": articulo_ofrecido.url_imagen,
                "estado": articulo_solicitado.estado
            }
        })

    # Responder con todas las transacciones relacionadas con el usuario solicitante
    return {
        "usuario_solicitante": {
            "id": user.id_usuario,
            "nombre": user.nombre,
            "email": user.correo_electronico
        },
        "trades": trade_details
    }
@router.get("/user/{user_id}/trades_as_solicitant")
async def get_trades_as_solicitant(user_id: int, db: Session = Depends(get_db)):
    # Verificar si el usuario existe
    user = db.query(User).filter(User.id_usuario == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Obtener todas las transacciones (trades) donde el usuario sea solicitante
    trades = db.query(Trade).filter(Trade.usuario_ofertador_id == user_id).all()

    if not trades:
        raise HTTPException(status_code=404, detail="No trades found for this user")

    # Construir la respuesta
    trade_details = []
    for trade in trades:
        # Obtener los artículos asociados
        articulo_solicitado = db.query(Item).filter(Item.id_articulo == trade.articulo_solicitado_id).first()
        articulo_ofrecido = db.query(Item).filter(Item.id_articulo == trade.articulo_ofrecido_id).first()

        # Obtener el usuario ofertante
        usuario_ofertador = db.query(User).filter(User.id_usuario == trade.usuario_ofertador_id).first()

        # Formatear cada transacción
        trade_details.append({
            "trade": {
                "id_trade": trade.id_trade,
                "estado": trade.estado,
                "fecha_oferta": trade.fecha_oferta
            },
            "usuario_ofertador": {
                "id": usuario_ofertador.id_usuario,
                "nombre": usuario_ofertador.nombre,
                "email": usuario_ofertador.correo_electronico
            },
            "articulo_solicitado": {
                "id": articulo_solicitado.id_articulo,
                "nombre": articulo_solicitado.nombre_articulo,
                "descripcion": articulo_solicitado.descripcion,
                "imagen": articulo_solicitado.url_imagen,
                "estado": articulo_solicitado.estado
            },
            "articulo_ofrecido": {
                "id": articulo_ofrecido.id_articulo,
                "nombre": articulo_ofrecido.nombre_articulo,
                "descripcion": articulo_ofrecido.descripcion,
                "imagen": articulo_ofrecido.url_imagen,
                "estado": articulo_ofrecido.estado
            }
        })

    # Responder con todas las transacciones relacionadas con el usuario ofertador
    return {
        "usuario_solicitante": {
            "id": user.id_usuario,
            "nombre": user.nombre,
            "email": user.correo_electronico
        },
        "trades": trade_details
    }

@router.put("updateStatus/")
def updateStatus(trade_id:int, status:str , db: Session = Depends(get_db)):
    trade = db.query(Trade).filter(Trade.id_trade == trade_id).first()
    if not trade:
        raise HTTPException(status_code=404, detail="Trade not found")
    trade.estado = status
    db.commit()
    db.refresh(trade)
    return trade
   


@router.post("/getAll", response_model=List[TradeResponse])
def get_all(db: Session = Depends(get_db)):
    trades = db.query(Trade).all()
    return trades

@router.get("/getAllTradesByIdUserOfert/", response_model=List[TradeResponse])
def get_all(id_user: int, db: Session = Depends(get_db)):
    trades = db.query(Trade).filter(Trade.usuario_ofertador_id  == id_user).all()
    return trades
    

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
