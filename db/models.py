from sqlalchemy import Column, Integer, String
from .database import Base

class Vuelo(Base):
    __tablename__ = "vuelos"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, index=True, nullable=False)
    destino = Column(String, nullable=False)
    emergencia = Column(Integer, default=0)  # 0 = normal, 1 = emergencia
