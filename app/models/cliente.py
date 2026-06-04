from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from pydantic import BaseModel

from app.database import Base

class ClienteBase(BaseModel):
    nombre: str
    edad: int
    descripcion: str | None = None

class ClienteCrear(ClienteBase):
    pass

class Cliente(ClienteBase):
    id: int

    model_config = {"orm_mode": True}

class ClienteORM(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    edad = Column(Integer, nullable=False)
    descripcion = Column(String, nullable=True)

    facturas = relationship(
        "FacturaORM",
        back_populates="cliente_rel",
        cascade="all, delete-orphan",
    )
