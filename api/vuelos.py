from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db import models, database
from schemas.vuelo_schema import VueloCrear, VueloRespuesta
from core.lista_vuelos import ListaVuelos

router = APIRouter()
lista_vuelos = ListaVuelos()  # Estructura en memoria

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/vuelos/", response_model=VueloRespuesta)
def agregar_vuelo(vuelo: VueloCrear, db: Session = Depends(get_db)):
    nuevo_vuelo = models.Vuelo(**vuelo.dict())
    db.add(nuevo_vuelo)
    db.commit()
    db.refresh(nuevo_vuelo)

    # Agrega a la estructura en memoria
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

@router.delete("/vuelos/{pos}", response_model=VueloCrear)
def eliminar_vuelo(pos: int):
    vuelo = lista_vuelos.extraer_de_posicion(pos)
    if not vuelo:
        raise HTTPException(status_code=404, detail="Posición inválida o lista vacía")
    return vuelo

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
