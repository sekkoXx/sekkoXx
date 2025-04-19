from pydantic import BaseModel, Field
from typing import Optional

class VueloBase(BaseModel):
    codigo: str = Field(..., example="LA1234")
    destino: str = Field(..., example="Santiago")
    emergencia: Optional[int] = Field(0, ge=0, le=1, example=1)

class VueloCrear(VueloBase):
    pass  # Igual al VueloBase, pero puede ser extendido en el futuro

class VueloRespuesta(VueloBase):
    id: int

    class Config:
        orm_mode = True  # Para compatibilidad con modelos ORM de SQLAlchemy
