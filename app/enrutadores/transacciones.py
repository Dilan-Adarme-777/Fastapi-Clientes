from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from app.conexion_bd import Sesion_dependencia
from app.modelos.facturas import Factura
from app.modelos.transacciones import (
    Transaccion,
    TransaccionCrear,
    TransaccionEditar,
    TransaccionLeer,
)

rutas_transacciones = APIRouter()


#endpoint para obtener todas las transacciones
@rutas_transacciones.get("/transacciones", response_model=list[TransaccionLeer])
async def listar_transacciones(sesion: Sesion_dependencia):
    consulta = select(Transaccion)
    lista_transacciones = sesion.exec(consulta).all()
    return lista_transacciones


#endpoint para obtener una transaccion por id
@rutas_transacciones.get("/transacciones/{id_transaccion}", response_model=TransaccionLeer)
async def obtener_transaccion(id_transaccion: int, sesion: Sesion_dependencia):

    transaccion_bd = sesion.get(Transaccion, id_transaccion)

    if not transaccion_bd:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"La transaccion con id {id_transaccion}, no existe."
        )

    return transaccion_bd


#endpoint para crear una transaccion
@rutas_transacciones.post("/transacciones", response_model=TransaccionLeer, status_code=status.HTTP_201_CREATED)
async def crear_transaccion(
    factura_id: int,
    datos_transaccion: TransaccionCrear,
    sesion: Sesion_dependencia
):

    #buscar la factura
    factura_encontrada = sesion.get(Factura, factura_id)

    #mensaje si no existe la factura
    if factura_encontrada is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"La factura con id {factura_id}, no existe."
        )

    #validar datos de la transaccion
    transaccion_dict = datos_transaccion.model_dump()
    transaccion_dict["factura_id"] = factura_id

    transaccion_val = Transaccion.model_validate(transaccion_dict)

    #guardar en la base de datos
    sesion.add(transaccion_val)
    sesion.commit()
    sesion.refresh(transaccion_val)

    return transaccion_val


#endpoint para editar una transaccion
@rutas_transacciones.patch("/transacciones/{id_transaccion}", response_model=TransaccionLeer)
async def editar_transaccion(
    id_transaccion: int,
    datos_transaccion: TransaccionEditar,
    sesion: Sesion_dependencia
):

    transaccion_bd = sesion.get(Transaccion, id_transaccion)

    if not transaccion_bd:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"La transaccion con id {id_transaccion}, no existe."
        )

    datos_actualizados = datos_transaccion.model_dump(exclude_unset=True)

    transaccion_bd.sqlmodel_update(datos_actualizados)

    sesion.add(transaccion_bd)
    sesion.commit()
    sesion.refresh(transaccion_bd)

    return transaccion_bd


#endpoint para eliminar una transaccion
@rutas_transacciones.delete("/transacciones/{id_transaccion}", response_model=TransaccionLeer)
async def eliminar_transaccion(
    id_transaccion: int,
    sesion: Sesion_dependencia
):

    transaccion_bd = sesion.get(Transaccion, id_transaccion)

    if not transaccion_bd:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"La transaccion con id {id_transaccion}, no existe."
        )

    sesion.delete(transaccion_bd)
    sesion.commit()

    return transaccion_bd