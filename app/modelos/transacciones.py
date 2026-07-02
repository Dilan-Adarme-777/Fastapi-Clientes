from __future__ import annotations

from typing import TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .facturas import Factura


class TransaccionBase(SQLModel):
    cantidad: int = Field(default=0)
    vr_unitario: float = Field(default=0.0)
    descripcion: str | None = None


class TransaccionCrear(TransaccionBase):
    pass


class TransaccionEditar(SQLModel):
    cantidad: int | None = None
    vr_unitario: float | None = None
    descripcion: str | None = None


class TransaccionLeer(TransaccionBase):
    id: int
    factura_id: int


class Transaccion(TransaccionBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    factura_id: int = Field(foreign_key="factura.id")

    factura: Factura = Relationship(back_populates="transacciones")  # 👈 sin comillas