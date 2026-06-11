from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.cliente import ClienteORM
from app.models.factura import Factura, FacturaCrear, FacturaORM

router = APIRouter(tags=['facturas'])

@router.get('', response_model=list[Factura])
def listar_facturas(db: Session = Depends(get_db)):
    return db.query(FacturaORM).all()

@router.post('', response_model=Factura, status_code=201)
def crear_factura(datos_factura: FacturaCrear, db: Session = Depends(get_db)):
    cliente = db.query(ClienteORM).filter(ClienteORM.id == datos_factura.cliente).first()
    if not cliente:
        raise HTTPException(status_code=404, detail='Cliente no encontrado')

    factura = FacturaORM(
        fecha=datos_factura.fecha,
        cliente_id=datos_factura.cliente,
        valortotal=datos_factura.valortotal,
    )
    db.add(factura)
    db.commit()
    db.refresh(factura)
    return factura

@router.put('/{id}', response_model=Factura)
def editar_factura(id: int, datos_factura: FacturaCrear, db: Session = Depends(get_db)):
    factura = db.query(FacturaORM).filter(FacturaORM.id == id).first()
    if not factura:
        raise HTTPException(status_code=404, detail='Factura no encontrada')

    cliente = db.query(ClienteORM).filter(ClienteORM.id == datos_factura.cliente).first()
    if not cliente:
        raise HTTPException(status_code=404, detail='Cliente no encontrado')

    factura.fecha = datos_factura.fecha
    factura.cliente_id = datos_factura.cliente
    factura.valortotal = datos_factura.valortotal

    db.commit()
    db.refresh(factura)
    return factura

@router.delete('/{id}', response_model=Factura)
def eliminar_factura(id: int, db: Session = Depends(get_db)):
    factura = db.query(FacturaORM).filter(FacturaORM.id == id).first()
    if not factura:
        raise HTTPException(status_code=404, detail='Factura no encontrada')

    db.delete(factura)
    db.commit()
    return factura
