from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import models, database
from api import vuelos

# Crear la base de datos si no existe
models.Base.metadata.create_all(bind=database.engine)

# Crear la app FastAPI
app = FastAPI(
    title="Gestor de Vuelos by sebastian",
    description="API para gestionar vuelos con prioridad, retrasos y cancelaciones usando listas doblemente enlazadas.",
    version="1.0.0"
)

# Permitir solicitudes desde cualquier origen (útil para frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambia esto en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir las rutas de vuelos
app.include_router(vuelos.router, prefix="/api", tags=["Vuelos"])

# Ruta raíz
@app.get("/")
def read_root():
    return {"mensaje": "Bienvenido al sistema de gestión de vuelos ✈️"}
