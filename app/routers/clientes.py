from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.cliente import Cliente, ClienteCrear, ClienteORM

router = APIRouter(tags=['clientes'])

@router.get('', response_model=list[Cliente])
def listar_clientes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Listar clientes con paginación. Por defecto: skip=0, limit=10"""
    if skip < 0 or limit <= 0:
        raise HTTPException(status_code=400, detail='skip debe ser >= 0 y limit debe ser > 0')
    return db.query(ClienteORM).offset(skip).limit(limit).all()

@router.get('/{id}', response_model=Cliente)
def obtener_cliente(id: int, db: Session = Depends(get_db)):
    cliente = db.query(ClienteORM).filter(ClienteORM.id == id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail='Cliente no encontrado')
    return cliente

@router.post('', response_model=Cliente, status_code=201)
def crear_cliente(datos_cliente: ClienteCrear, db: Session = Depends(get_db)):
    cliente = ClienteORM(**datos_cliente.model_dump())
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    return cliente

@router.put('/{id}', response_model=Cliente)
def editar_cliente(id: int, datos_cliente: ClienteCrear, db: Session = Depends(get_db)):
    cliente = db.query(ClienteORM).filter(ClienteORM.id == id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail='Cliente no encontrado')

    for key, value in datos_cliente.model_dump().items():
        setattr(cliente, key, value)

    db.commit()
    db.refresh(cliente)
    return cliente

@router.delete('/{id}', response_model=Cliente)
def eliminar_cliente(id: int, db: Session = Depends(get_db)):
    cliente = db.query(ClienteORM).filter(ClienteORM.id == id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail='Cliente no encontrado')

    db.delete(cliente)
    db.commit()
    return cliente
