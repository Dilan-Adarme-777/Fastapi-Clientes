from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.factura import FacturaORM
from app.models.transaccion import Transaccion, TransaccionCrear, TransaccionORM

router = APIRouter()

@router.get('', response_model=list[Transaccion])
def listar_transacciones(db: Session = Depends(get_db)):
    return db.query(TransaccionORM).all()

@router.post('', response_model=Transaccion, status_code=201)
def crear_transaccion(datos_transaccion: TransaccionCrear, db: Session = Depends(get_db)):
    factura = db.query(FacturaORM).filter(FacturaORM.id == datos_transaccion.factura).first()
    if not factura:
        raise HTTPException(status_code=404, detail='Factura no encontrada')

    transaccion = TransaccionORM(
        descripcion=datos_transaccion.descripcion,
        factura_id=datos_transaccion.factura,
    )
    db.add(transaccion)
    db.commit()
    db.refresh(transaccion)
    return transaccion

@router.put('/{id}', response_model=Transaccion)
def editar_transaccion(id: int, datos_transaccion: TransaccionCrear, db: Session = Depends(get_db)):
    transaccion = db.query(TransaccionORM).filter(TransaccionORM.id == id).first()
    if not transaccion:
        raise HTTPException(status_code=404, detail='Transaccion no encontrada')

    factura = db.query(FacturaORM).filter(FacturaORM.id == datos_transaccion.factura).first()
    if not factura:
        raise HTTPException(status_code=404, detail='Factura no encontrada')

    transaccion.descripcion = datos_transaccion.descripcion
    transaccion.factura_id = datos_transaccion.factura

    db.commit()
    db.refresh(transaccion)
    return transaccion

@router.delete('/{id}', response_model=Transaccion)
def eliminar_transaccion(id: int, db: Session = Depends(get_db)):
    transaccion = db.query(TransaccionORM).filter(TransaccionORM.id == id).first()
    if not transaccion:
        raise HTTPException(status_code=404, detail='Transaccion no encontrada')

    db.delete(transaccion)
    db.commit()
    return transaccion
