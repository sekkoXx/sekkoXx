from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db import models, database
from schemas.vuelo_schema import VueloCrear, VueloRespuesta
from core.lista_vuelos import ListaVuelos

router = APIRouter()
lista_vuelos = ListaVuelos()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/vuelos/", response_model=VueloRespuesta)
def agregar_vuelo(vuelo: VueloCrear, db: Session = Depends(get_db)):
    # Verificar si ya existe el vuelo con ese ID
    if db.query(models.Vuelo).filter(models.Vuelo.id == vuelo.id).first():
        raise HTTPException(status_code=400, detail="El ID ya está registrado.")

    nuevo_vuelo = models.Vuelo(**vuelo.dict())
    db.add(nuevo_vuelo)
    db.commit()
    db.refresh(nuevo_vuelo)

    # Insertar en la lista enlazada
    if vuelo.emergencia:
        lista_vuelos.insertar_al_frente(vuelo.dict())
    else:
        lista_vuelos.insertar_al_final(vuelo.dict())

    return nuevo_vuelo

@router.get("/vuelos/", response_model=list[VueloRespuesta])
def listar_vuelos(db: Session = Depends(get_db)):
    return db.query(models.Vuelo).all()

@router.get("/vuelos/proximo", response_model=VueloCrear)
def obtener_proximo():
    vuelo = lista_vuelos.obtener_primero()
    if not vuelo:
        raise HTTPException(status_code=404, detail="No hay vuelos en la lista")
    return vuelo

@router.delete("/vuelos/{id}", response_model=VueloCrear)
def eliminar_vuelo(id: int, db: Session = Depends(get_db)):
    vuelo_en_db = db.query(models.Vuelo).filter(models.Vuelo.id == id).first()
    if not vuelo_en_db:
        raise HTTPException(status_code=404, detail="Vuelo no encontrado")

    # Eliminar de la base de datos
    db.delete(vuelo_en_db)
    db.commit()

    # Eliminar también de la lista en memoria
    vuelos_actuales = lista_vuelos.listar_vuelos()
    for i, v in enumerate(vuelos_actuales):
        if v["id"] == id:
            lista_vuelos.extraer_de_posicion(i)
            return v

    raise HTTPException(status_code=404, detail="Vuelo no encontrado en memoria")

@router.get("/vuelos/estructura", response_model=list[VueloCrear])
def estructura_memoria():
    return lista_vuelos.listar_vuelos()

@router.post("/vuelos/reordenar")
def reordenar_lista(nuevo_orden: list[int]):
    try:
        lista_vuelos.reordenar(nuevo_orden)
        return {"mensaje": "Lista reordenada correctamente"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
