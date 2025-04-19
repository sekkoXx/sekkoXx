from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Puedes cambiar la URL si quieres usar PostgreSQL o MySQL
SQLALCHEMY_DATABASE_URL = "sqlite:///./vuelos.db"

# connect_args es obligatorio en SQLite para evitar errores con múltiples hilos
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
