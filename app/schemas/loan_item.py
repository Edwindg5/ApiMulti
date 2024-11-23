from pydantic import BaseModel, field_validator
from datetime import datetime

class LoanItemBase(BaseModel):
    articulo_id: int
    prestador_id: int
    prestatario_id: int
    fecha_prestamo: datetime
    fecha_devolucion: datetime | None
    estado: str

    # Validación de fechas con el nuevo decorador
    @field_validator("fecha_devolucion")
    def validate_fecha_devolucion(cls, fecha_devolucion, values):
        fecha_prestamo = values.get("fecha_prestamo")
        if fecha_devolucion and fecha_prestamo and fecha_devolucion < fecha_prestamo:
            raise ValueError("La fecha de devolución no puede ser anterior a la fecha de préstamo.")
        return fecha_devolucion

class LoanItemCreate(LoanItemBase):
    pass

class LoanItemResponse(LoanItemBase):
    id_loan_items: int

    class Config:
        orm_mode = True