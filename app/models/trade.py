from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey
from app.shared.config.db import Base
from app.utils.security import TransactionStatus
from sqlalchemy.sql import func

class Trade(Base):
    __tablename__ = "trades"

    id_trade = Column(Integer, primary_key=True, index=True)
    articulo_solicitado_id = Column(Integer, ForeignKey("items.id_articulo"))
    articulo_ofrecido_id = Column(Integer, ForeignKey("items.id_articulo"))
    usuario_solicitante_id = Column(Integer, ForeignKey("users.id_usuario"))
    usuario_ofertador_id = Column(Integer, ForeignKey("users.id_usuario"))
    fecha_oferta = Column(TIMESTAMP, server_default=func.now())
    estado = Column(TransactionStatus)
