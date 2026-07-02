from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field

from app.database import Base

class FacturaBase(BaseModel):
    fecha: datetime = Field(..., description="Fecha de la factura")
    cliente: int = Field(..., gt=0, description="ID del cliente")

class FacturaCrear(FacturaBase):
    pass

class Factura(FacturaBase):
    id: int
    valortotal: int = Field(default=0, description="Total calculado de la factura")

    model_config = {"from_attributes": True}

class FacturaORM(Base):
    __tablename__ = "facturas"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(DateTime, nullable=False)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)

    cliente_rel = relationship("ClienteORM", back_populates="facturas")
    transacciones = relationship(
        "TransaccionORM",
        back_populates="factura_rel",
        cascade="all, delete-orphan",
    )

    @property
    def valortotal(self) -> int:
        """Calcula el total sumando los amounts de todas las transacciones"""
        return sum(t.amount for t in self.transacciones) if self.transacciones else 0

    @property
    def cliente(self) -> int:
        return self.cliente_id
