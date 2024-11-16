from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from app.shared.config.db import Base
from datetime import datetime

class LoanItem(Base):
    __tablename__ = "loan_items"

    id_loan_items = Column(Integer, primary_key=True, index=True)
    articulo_id = Column(Integer, nullable=False)
    prestador_id = Column(Integer, ForeignKey("users.id_usuario"), nullable=False)
    prestatario_id = Column(Integer, ForeignKey("users.id_usuario"), nullable=False)
    fecha_prestamo = Column(DateTime, nullable=False, default=datetime.utcnow)
    fecha_devolucion = Column(DateTime, nullable=True)
    estado = Column(String, nullable=False)

    # Relaciones explícitas con el modelo User
    prestador = relationship("User", foreign_keys=[prestador_id])
    prestatario = relationship("User", foreign_keys=[prestatario_id])
