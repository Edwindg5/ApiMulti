from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.shared.config.db import Base
from app.utils.security import TransactionStatus

class Trade(Base):
    __tablename__ = "trades"

    id_trade = Column(Integer, primary_key=True, autoincrement=True)
    articulo_solicitado_id = Column(Integer, ForeignKey("items.id_articulo"), nullable=False)
    articulo_ofrecido_id = Column(Integer, ForeignKey("items.id_articulo"), nullable=False)
    usuario_solicitante_id = Column(Integer, ForeignKey("users.id_usuario"), nullable=False)
    usuario_ofertador_id = Column(Integer, ForeignKey("users.id_usuario"), nullable=False)
    fecha_oferta = Column(TIMESTAMP, server_default=func.current_timestamp())
    estado = Column(Enum(TransactionStatus), nullable=False)

    # Relaciones (opcional si se necesita acceder a objetos relacionados)
    articulo_solicitado = relationship("Item", foreign_keys=[articulo_solicitado_id])
    articulo_ofrecido = relationship("Item", foreign_keys=[articulo_ofrecido_id])
