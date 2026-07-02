from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from app.modelos.clientes import cliente, clientecrear, clienteeditar, ClienteLeer
from app.conexion_bd import Sesion_dependencia

rutas_clientes = APIRouter()


#endpoint para obtener todos los clientes
@rutas_clientes.get("/clientes", response_model=list[ClienteLeer])
async def listar_clientes(sesion: Sesion_dependencia):
    lista_cli = sesion.exec(select(cliente)).all()
    return lista_cli


#endpoint para listar un solo cliente por id
@rutas_clientes.get("/clientes/{cliente_id}", response_model=ClienteLeer)
async def listar_cliente_por_id(cliente_id: int, sesion: Sesion_dependencia):
    cliente_bd = sesion.get(cliente, cliente_id)

    if not cliente_bd:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El cliente con id {cliente_id}, no existe."
        )

    return cliente_bd


#endpoint para crear un cliente
@rutas_clientes.post("/clientes", response_model=ClienteLeer, status_code=status.HTTP_201_CREATED)
async def crear_cliente(datos_cliente: clientecrear, sesion: Sesion_dependencia):
    cliente_val = cliente.model_validate(datos_cliente.model_dump())

    sesion.add(cliente_val)
    sesion.commit()
    sesion.refresh(cliente_val)

    return cliente_val


#endpoint para editar un cliente
@rutas_clientes.patch("/clientes/{cliente_id}", response_model=ClienteLeer)
async def editar_cliente(cliente_id: int, datos_cliente: clienteeditar, sesion: Sesion_dependencia):
    cliente_bd = sesion.get(cliente, cliente_id)

    if not cliente_bd:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El cliente con id {cliente_id}, no existe."
        )

    cliente_dict = datos_cliente.model_dump(exclude_unset=True)
    cliente_bd.sqlmodel_update(cliente_dict)

    sesion.add(cliente_bd)
    sesion.commit()
    sesion.refresh(cliente_bd)

    return cliente_bd


#endpoint para eliminar un cliente
@rutas_clientes.delete("/clientes/{cliente_id}", response_model=ClienteLeer)
async def eliminar_cliente(cliente_id: int, sesion: Sesion_dependencia):
    cliente_bd = sesion.get(cliente, cliente_id)

    if not cliente_bd:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El cliente con id {cliente_id}, no existe."
        )

    sesion.delete(cliente_bd)
    sesion.commit()

    return cliente_bd