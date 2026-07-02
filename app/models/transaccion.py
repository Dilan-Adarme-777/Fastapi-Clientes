from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field

from app.database import Base

class TransaccionBase(BaseModel):
    descripcion: str = Field(..., min_length=1, description="Descripción de la transacción")
    amount: int = Field(..., gt=0, description="Monto en enteros para evitar problemas de precisión")
    factura: int = Field(..., gt=0, description="ID de la factura a la que pertenece")

class TransaccionCrear(TransaccionBase):
    pass

class Transaccion(TransaccionBase):
    id: int

    model_config = {"from_attributes": True}

class TransaccionORM(Base):
    __tablename__ = "transacciones"

    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    factura_id = Column(Integer, ForeignKey("facturas.id"), nullable=False)

    factura_rel = relationship("FacturaORM", back_populates="transacciones")

    @property
    def factura(self) -> int:
        return self.factura_id
