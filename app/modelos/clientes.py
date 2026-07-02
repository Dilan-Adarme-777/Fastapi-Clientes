from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship

#crear modelos cliente (id, nombre , email, descripcion)
class clienteBase(SQLModel):
    nombre:str = Field(default=None)
    email:str = Field(default=None)
    descripcion: str | None = Field(default=None)

class clientecrear(clienteBase):
    pass

class clienteeditar(clienteBase):
    pass

class cliente(clienteBase, table=True):
    id:int | None = Field(default=None, primary_key=True)


class ClienteLeer(clienteBase):
    id: int