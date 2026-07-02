from pydantic import computed_field
from sqlmodel import SQLModel, Field, Relationship
from .transacciones import Transaccion, TransaccionLeer
from .clientes import cliente as ClienteModelo, ClienteLeer
from datetime import datetime


class FacturaBase(SQLModel):
    fecha: datetime = Field(default_factory=datetime.now)

    @computed_field
    @property
    def vr_total(self) -> float:
        total_factura = 0.0
        transacciones_factura = getattr(self, "transacciones", None)

        if not transacciones_factura:
            return 0.0

        for transaccion in transacciones_factura:
            total_factura += transaccion.vr_unitario * transaccion.cantidad

        return total_factura


class FacturaCrear(FacturaBase):
    pass


class FacturaEditar(SQLModel):
    fecha: datetime | None = None


class FacturaLeer(FacturaBase):
    id: int
    cliente_id: int
    cliente: ClienteLeer
    transacciones: list[TransaccionLeer] = []


class Factura(FacturaBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    cliente_id: int = Field(foreign_key="cliente.id")

    transacciones: list["Transaccion"] = Relationship(
        back_populates="factura",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    cliente: ClienteModelo = Relationship()