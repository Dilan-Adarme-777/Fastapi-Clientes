from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from pydantic import BaseModel

from app.database import Base


class FacturaBase(BaseModel):
    fecha: datetime
    cliente: int


class FacturaCrear(FacturaBase):
    pass


class Factura(FacturaBase):
    id: int
    valortotal: int = 0

    class Config:
        from_attributes = True


class FacturaORM(Base):
    __tablename__ = "facturas"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(DateTime, nullable=False)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)

    cliente_rel = relationship("ClienteORM", back_populates="facturas")
    transacciones = relationship("TransaccionORM", back_populates="factura_rel")

    @property
    def valortotal(self):
        return sum(t.amount for t in self.transacciones) if self.transacciones else 0

    @property
    def cliente(self):
        return self.cliente_id
