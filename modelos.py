from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

# Tabla intermedia muchos-a-muchos + orden FIFO
class PersonajeMision(Base):
    __tablename__ = "personaje_mision"
    id = Column(Integer, primary_key=True, index=True)
    personaje_id = Column(Integer, ForeignKey("personajes.id"))
    mision_id = Column(Integer, ForeignKey("misiones.id"))
    orden = Column(Integer)  # Para FIFO: menor valor = más antiguo

class Personaje(Base):
    __tablename__ = "personajes"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)
    xp = Column(Integer, default=0)

    misiones = relationship(
        "PersonajeMision", backref="personaje", cascade="all, delete"
    )

class Mision(Base):
    __tablename__ = "misiones"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)
    descripcion = Column(String)

    personajes = relationship(
        "PersonajeMision", backref="mision", cascade="all, delete"
    )
