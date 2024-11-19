from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ENUM
from datetime import date
from app.shared.config.db import Base

class Item(Base):
    __tablename__ = 'items'

    id_articulo = Column(Integer, primary_key=True, autoincrement=True)
    nombre_articulo = Column(String(100), nullable=False)
    descripcion = Column(String(255), nullable=True)
    id_categoria = Column(Integer, nullable=False)
    precio = Column(Integer, nullable=False)

    # Cambiado a ENUM con los valores correctos
    tipo_transaccion = Column(
        ENUM('COMPRA', 'VENTA', 'INTERCAMBIO', 'PRESTAMO', name="transactiontype"),
        nullable=False
    )
    usuario_id = Column(Integer, ForeignKey("users.id_usuario"), nullable=False)
    estado = Column(
        ENUM(
            'PENDING', 'COMPLETED', 'CANCELLED', 'VENTA', 'INTERCAMBIO', 'DONACIÓN',
            'DISPONIBLE', 'NO_DISPONIBLE', 'ELIMINADO', 'COMPRA',
            name="transaction_status"
        ),
        nullable=False
    )
    fecha_publicacion = Column(TIMESTAMP, server_default=func.current_timestamp())

    # Relaciones
    user = relationship("User", back_populates="items")  # Relación con el modelo User
    shopping_cart = relationship("ShoppingCart", back_populates="articulo")  # Relación con el carrito
    transactions = relationship("TransactionHistory", back_populates="item")  # Relación con historial de transacciones
    trades_solicitados = relationship(
        "Trade",
        foreign_keys="Trade.articulo_solicitado_id",
        back_populates="articulo_solicitado"
    )  # Relación para intercambios solicitados
    trades_ofrecidos = relationship(
        "Trade",
        foreign_keys="Trade.articulo_ofrecido_id",
        back_populates="articulo_ofrecido"
    )  # Relación para intercambios ofrecidos

    # Propiedad para devolver solo la fecha de publicación
    @property
    def fecha_publicacion_date(self) -> date:
        """Devuelve solo la fecha de publicación o None si no está definida."""
        if self.fecha_publicacion:
            return self.fecha_publicacion.date()
        return None
