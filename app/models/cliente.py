from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field

from app.database import Base

class ClienteBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100, description="Nombre del cliente")
    email: str = Field(..., description="Email del cliente")
    edad: int = Field(..., ge=0, le=150, description="Edad del cliente")
    descripcion: str | None = Field(None, max_length=500, description="Descripción adicional del cliente")

class ClienteCrear(ClienteBase):
    pass

class Cliente(ClienteBase):
    id: int

    model_config = {"from_attributes": True}

class ClienteORM(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    edad = Column(Integer, nullable=False)
    descripcion = Column(String, nullable=True)

    facturas = relationship(
        "FacturaORM",
        back_populates="cliente_rel",
        cascade="all, delete-orphan",
    )
