from fastapi import FastAPI

from app.database import Base, engine
from app.models.cliente import ClienteORM
from app.models.factura import FacturaORM
from app.models.transaccion import TransaccionORM
from app.routers.clientes import router as clientes_router
from app.routers.facturas import router as facturas_router
from app.routers.transacciones import router as transacciones_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title='FastAPI Clientes')

app.include_router(clientes_router, prefix='/clientes', tags=['clientes'])
app.include_router(facturas_router, prefix='/facturas', tags=['facturas'])
app.include_router(transacciones_router, prefix='/transacciones', tags=['transacciones'])

@app.get('/')
def root():
    return {'message': 'API de clientes, facturas y transacciones'}
