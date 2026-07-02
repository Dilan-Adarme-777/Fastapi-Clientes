# FastAPI Clientes 🚀

API REST para gestionar **Clientes**, **Facturas** y **Transacciones** utilizando FastAPI y SQLAlchemy.

## 📋 Descripción del Proyecto

Este proyecto implementa una API REST siguiendo buenas prácticas de desarrollo:
- Separación de responsabilidades (models, routers, database)
- Validación de datos con Pydantic
- Base de datos relacional con SQLAlchemy ORM
- Documentación automática con Swagger/OpenAPI
- Relaciones entre entidades (Cliente → Factura → Transacción)

### Características Principales
✅ CRUD completo para Clientes, Facturas y Transacciones  
✅ Validación automática de datos con Pydantic  
✅ Relaciones entre entidades con ForeignKeys  
✅ Total de factura calculado automáticamente (suma de transacciones)  
✅ Documentación interactiva con Swagger (`/docs`)  
✅ Base de datos SQLite con SQLAlchemy ORM  

---

## 🛠️ Tecnologías Utilizadas

- **FastAPI** 0.115.8 - Framework web moderno
- **Uvicorn** 0.34.0 - Servidor ASGI
- **SQLAlchemy** - ORM para base de datos
- **Pydantic** - Validación de datos
- **SQLite** - Base de datos relacional

---

## 📦 Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/fastapi-clientes.git
cd fastapi-clientes
```

### 2. Crear entorno virtual
```bash
python -m venv venv
# En Windows
venv\Scripts\activate
# En Linux/Mac
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requerimientos.txt
```

---

## 🚀 Ejecución

### Desarrollo (con recarga automática)
```bash
fastapi dev app/main.py
```

### Producción
```bash
uvicorn app.main:app --reload
```

La API estará disponible en: `http://localhost:8000`

### Documentación Interactiva
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

---

## 📁 Estructura de Carpetas

```
fastapi-clientes/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Entrada principal, inicializa la app
│   ├── database.py             # Configuración de SQLAlchemy
│   ├── models/
│   │   ├── cliente.py          # Modelo Cliente (ORM + Pydantic)
│   │   ├── factura.py          # Modelo Factura (ORM + Pydantic)
│   │   └── transaccion.py      # Modelo Transacción (ORM + Pydantic)
│   └── routers/
│       ├── __init__.py
│       ├── clientes.py         # Endpoints de Clientes
│       ├── facturas.py         # Endpoints de Facturas
│       └── transacciones.py    # Endpoints de Transacciones
├── requerimientos.txt          # Dependencias del proyecto
├── database.db                 # Base de datos SQLite (se genera automáticamente)
└── README.md                   # Este archivo
```

---

## 📡 Endpoints Disponibles

### 👥 Clientes

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/clientes` | Listar todos los clientes |
| `GET` | `/clientes/{id}` | Obtener un cliente por ID |
| `POST` | `/clientes` | Crear un nuevo cliente |
| `PUT` | `/clientes/{id}` | Actualizar un cliente |
| `DELETE` | `/clientes/{id}` | Eliminar un cliente |

**Crear Cliente (POST /clientes)**
```json
{
  "nombre": "Juan Pérez",
  "email": "juan@example.com",
  "edad": 30,
  "descripcion": "Cliente VIP"
}
```

---

### 📄 Facturas

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/facturas` | Listar todas las facturas |
| `GET` | `/facturas/{id}` | Obtener una factura por ID |
| `GET` | `/facturas/{id}/total` | Obtener el total de una factura |
| `POST` | `/facturas` | Crear una nueva factura |
| `PUT` | `/facturas/{id}` | Actualizar una factura |
| `DELETE` | `/facturas/{id}` | Eliminar una factura |

**Crear Factura (POST /facturas)**
```json
{
  "fecha": "2024-01-15T10:30:00",
  "cliente": 1
}
```

**Nota:** El `valortotal` se calcula automáticamente sumando todas las transacciones asociadas.

---

### 💳 Transacciones

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/transacciones` | Listar todas las transacciones |
| `GET` | `/transacciones/{id}` | Obtener una transacción por ID |
| `POST` | `/transacciones` | Crear una nueva transacción |
| `PUT` | `/transacciones/{id}` | Actualizar una transacción |
| `DELETE` | `/transacciones/{id}` | Eliminar una transacción |

**Crear Transacción (POST /transacciones)**
```json
{
  "descripcion": "Pago de servicios",
  "amount": 50000,
  "factura": 1
}
```

**Nota:** El `amount` debe ser un número entero para evitar problemas de precisión.

---

## 🔄 Modelo de Relaciones

```
Cliente (1)
    ↓ (1:N)
    └─→ Factura (N)
            ↓ (1:N)
            └─→ Transacción (N)
```

- **Cliente** puede tener múltiples **Facturas**
- **Factura** pertenece a un **Cliente** y tiene múltiples **Transacciones**
- **Transacción** pertenece a una **Factura**
- Al eliminar un **Cliente**, se eliminan en cascada sus **Facturas** y sus **Transacciones**

---

## 📊 Evolución del Proyecto (Commits)

Este proyecto fue desarrollado incrementalmente para mantener un historial claro:

1. **feat: inicio del proyecto FastAPI sin estructura** - Hello World básico
2. **feat: CRUD funcional de clientes sin estructura (main.py)** - Clientes en memoria
3. **feat: CRUD de facturas y transacciones sin estructura** - Todas las entidades en main.py
4. **refactor: reestructuración del proyecto en módulos** - Separación en models.py, schemas.py, routers
5. **feat: migración a base de datos con relaciones entre Cliente, Factura y Transacción** - SQLAlchemy ORM

Puedes ver cada etapa con:
```bash
git log --oneline
git checkout <hash>
```

---

## 🧪 Pruebas

Actualmente la API está funcional. Se pueden agregar pruebas unitarias con Pytest en el futuro.

---

## 📝 Ejemplo de Uso Completo

### 1. Crear un cliente
```bash
curl -X POST "http://localhost:8000/clientes" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Ana García",
    "email": "ana@example.com",
    "edad": 28,
    "descripcion": "Cliente frecuente"
  }'
```

### 2. Crear una factura para ese cliente
```bash
curl -X POST "http://localhost:8000/facturas" \
  -H "Content-Type: application/json" \
  -d '{
    "fecha": "2024-01-15T10:30:00",
    "cliente": 1
  }'
```

### 3. Crear transacciones en esa factura
```bash
curl -X POST "http://localhost:8000/transacciones" \
  -H "Content-Type: application/json" \
  -d '{
    "descripcion": "Venta de producto A",
    "amount": 100000,
    "factura": 1
  }'
```

### 4. Obtener el total de la factura
```bash
curl -X GET "http://localhost:8000/facturas/1/total"
```

Respuesta:
```json
{
  "id": 1,
  "total": 100000
}
```

---

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

---

## 👨‍💻 Autor

Dilan Santiago Adarme Dominguez
