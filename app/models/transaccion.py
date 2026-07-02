from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from pydantic import BaseModel

from app.database import Base


class TransaccionBase(BaseModel):
    descripcion: str
    amount: int
    factura: int


class TransaccionCrear(TransaccionBase):
    pass


class Transaccion(TransaccionBase):
    id: int

    class Config:
        from_attributes = True


class TransaccionORM(Base):
    __tablename__ = "transacciones"

    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    factura_id = Column(Integer, ForeignKey("facturas.id"), nullable=False)

    factura_rel = relationship("FacturaORM", back_populates="transacciones")

    @property
    def factura(self):
        return self.factura_id
