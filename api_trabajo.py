from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from modelos import Personaje, Mision, PersonajeMision
from cola_trabajo import ArrayQueue

router = APIRouter()

# Dependency para obtener sesión de la DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Crear personaje
@router.post("/personajes")
def crear_personaje(id: int, nombre: str, db: Session = Depends(get_db)):
    if db.query(Personaje).filter(Personaje.id == id).first():
        raise HTTPException(status_code=400, detail="Personaje ya existe")

    nuevo_personaje = Personaje(id=id, nombre=nombre)
    db.add(nuevo_personaje)
    db.commit()
    return {"mensaje": "Personaje creado"}

# Crear misión
@router.post("/misiones")
def crear_mision(id: int, nombre: str, descripcion: str, db: Session = Depends(get_db)):
    if db.query(Mision).filter(Mision.id == id).first():
        raise HTTPException(status_code=400, detail="Misión ya existe")

    nueva_mision = Mision(id=id, nombre=nombre, descripcion=descripcion)
    db.add(nueva_mision)
    db.commit()
    return {"mensaje": "Misión creada"}

# Aceptar misión (encolar)
@router.post("/personajes/{id_personaje}/misiones/{id_mision}")
def aceptar_mision(id_personaje: int, id_mision: int, db: Session = Depends(get_db)):
    personaje = db.query(Personaje).filter(Personaje.id == id_personaje).first()
    mision = db.query(Mision).filter(Mision.id == id_mision).first()

    if not personaje:
        raise HTTPException(status_code=404, detail="Personaje no existe")
    if not mision:
        raise HTTPException(status_code=404, detail="Misión no existe")

    orden = db.query(PersonajeMision).filter(PersonajeMision.personaje_id == id_personaje).count()

    relacion = PersonajeMision(personaje_id=id_personaje, mision_id=id_mision, orden=orden)
    db.add(relacion)
    db.commit()
    return {"mensaje": "Misión aceptada"}

# Completar misión (desencolar y sumar XP)
@router.post("/personajes/{id_personaje}/completar")
def completar_mision(id_personaje: int, db: Session = Depends(get_db)):
    personaje = db.query(Personaje).filter(Personaje.id == id_personaje).first()
    if not personaje:
        raise HTTPException(status_code=404, detail="Personaje no existe")

    mision_relacion = (
        db.query(PersonajeMision)
        .filter(PersonajeMision.personaje_id == id_personaje)
        .order_by(PersonajeMision.orden)
        .first()
    )

    if not mision_relacion:
        raise HTTPException(status_code=400, detail="No hay misiones para completar")

    mision = db.query(Mision).filter(Mision.id == mision_relacion.mision_id).first()

    personaje.xp += 100
    db.delete(mision_relacion)
    db.commit()

    return {
        "mensaje": "Misión completada",
        "mision": {"id": mision.id, "nombre": mision.nombre},
        "xp_total": personaje.xp,
    }

# Listar misiones pendientes FIFO
@router.get("/personajes/{id_personaje}/misiones")
def listar_misiones(id_personaje: int, db: Session = Depends(get_db)):
    personaje = db.query(Personaje).filter(Personaje.id == id_personaje).first()
    if not personaje:
        raise HTTPException(status_code=404, detail="Personaje no existe")

    relaciones = (
        db.query(PersonajeMision)
        .filter(PersonajeMision.personaje_id == id_personaje)
        .order_by(PersonajeMision.orden)
        .all()
    )

    misiones = []
    for rel in relaciones:
        mision = db.query(Mision).filter(Mision.id == rel.mision_id).first()
        misiones.append({"id": mision.id, "nombre": mision.nombre, "descripcion": mision.descripcion})

    return {"misiones": misiones}
