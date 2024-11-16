from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.notification import NotificationCreate, NotificationResponse
from app.models.notifications import Notification
from app.shared.config.db import get_db

router = APIRouter()

@router.post("/", response_model=NotificationResponse)
def create_notification(notification: NotificationCreate, db: Session = Depends(get_db)):
    db_notification = Notification(**notification.dict())
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification
@router.get("/{notification_id}", response_model=NotificationResponse)
def read_notification(notification_id: int, db: Session = Depends(get_db)):
    notification = db.query(Notification).filter(Notification.id_notificacion == notification_id).first()  # Cambiado a id_notificacion
    if notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification

@router.put("/{notification_id}", response_model=NotificationResponse)
def update_notification(notification_id: int, notification: NotificationCreate, db: Session = Depends(get_db)):
    db_notification = db.query(Notification).filter(Notification.id_notificacion == notification_id).first()  # Cambiado a id_notificacion
    if db_notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    for key, value in notification.dict().items():
        setattr(db_notification, key, value)
    db.commit()
    db.refresh(db_notification)
    return db_notification

@router.delete("/{notification_id}")
def delete_notification(notification_id: int, db: Session = Depends(get_db)):
    db_notification = db.query(Notification).filter(Notification.id_notificacion == notification_id).first()  # Cambiado a id_notificacion
    if db_notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    db.delete(db_notification)
    db.commit()
    return {"message": "Notification deleted successfully"}
