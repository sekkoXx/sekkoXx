from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db import models, database
from core.lista_vuelos import ListaVuelos

router = APIRouter()
lista_vuelos = ListaVuelos()

# Dependency para la base de datos
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Crear vuelo
@router.post("/vuelos")
def crear_vuelo(id: int, codigo: str, destino: str, emergencia: int = 0, db: Session = Depends(get_db)):
    if db.query(models.Vuelo).filter(models.Vuelo.id == id).first():
        raise HTTPException(status_code=400, detail="El vuelo ya existe")

    nuevo_vuelo = models.Vuelo(id=id, codigo=codigo, destino=destino, emergencia=emergencia)
    db.add(nuevo_vuelo)
    db.commit()

    datos_vuelo = {
        "id": id,
        "codigo": codigo,
        "destino": destino,
        "emergencia": emergencia
    }

    if emergencia:
        lista_vuelos.insertar_al_frente(datos_vuelo)
    else:
        lista_vuelos.insertar_al_final(datos_vuelo)

    return {"mensaje": "Vuelo creado exitosamente"}

# Eliminar vuelo por ID
@router.delete("/vuelos/{id}")
def eliminar_vuelo(id: int, db: Session = Depends(get_db)):
    vuelo_db = db.query(models.Vuelo).filter(models.Vuelo.id == id).first()
    if not vuelo_db:
        raise HTTPException(status_code=404, detail="Vuelo no encontrado en la base de datos")

    db.delete(vuelo_db)
    db.commit()

    # También eliminar de la lista en memoria
    vuelos_memoria = lista_vuelos.listar_vuelos()
    for i, vuelo in enumerate(vuelos_memoria):
        if vuelo["id"] == id:
            lista_vuelos.extraer_de_posicion(i)
            break

    return {"mensaje": f"Vuelo con ID {id} eliminado"}

# Ver todos los vuelos (BD)
@router.get("/vuelos")
def listar_vuelos(db: Session = Depends(get_db)):
    return db.query(models.Vuelo).all()

# Ver vuelos en memoria (estructura actual)
@router.get("/vuelos/estructura")
def listar_vuelos_en_memoria():
    return lista_vuelos.listar_vuelos()

# Obtener el próximo vuelo a despegar
@router.get("/vuelos/proximo")
def obtener_proximo_vuelo():
    vuelo = lista_vuelos.obtener_primero()
    if not vuelo:
        raise HTTPException(status_code=404, detail="No hay vuelos pendientes")
    return vuelo
