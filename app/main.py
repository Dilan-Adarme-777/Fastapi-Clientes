from fastapi import FastAPI
from app.enrutadores import clientes
from app.enrutadores import facturas
from app.enrutadores import transacciones
from app.conexion_bd import crear_tablas

app = FastAPI(lifespan=crear_tablas)

# Incluir rutas
app.include_router(clientes.rutas_clientes, tags=["Clientes"])
app.include_router(facturas.rutas_factura, tags=["Facturas"])
app.include_router(transacciones.rutas_transacciones, tags=["Transacciones"])