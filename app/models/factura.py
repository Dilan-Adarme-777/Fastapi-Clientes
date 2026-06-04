from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship
from pydantic import BaseModel

from app.database import Base

class FacturaBase(BaseModel):
    fecha: datetime
    cliente: int
    valortotal: float

class FacturaCrear(FacturaBase):
    pass

class Factura(FacturaBase):
    id: int

    model_config = {"orm_mode": True}

class FacturaORM(Base):
    __tablename__ = "facturas"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(DateTime, nullable=False)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    valortotal = Column(Float, nullable=False)

    cliente_rel = relationship("ClienteORM", back_populates="facturas")
    transacciones = relationship(
        "TransaccionORM",
        back_populates="factura_rel",
        cascade="all, delete-orphan",
    )

    @property
    def cliente(self) -> int:
        return self.cliente_id
