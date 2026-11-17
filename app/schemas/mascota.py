from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, ConfigDict


class MascotaBase(BaseModel):
    nombre: str
    especie: str
    raza: Optional[str] = None
    sexo: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
    peso_kg: Optional[Decimal] = None
    color: Optional[str] = None
    esterilizado: bool = False
    foto_url: Optional[str] = None


class MascotaCreate(MascotaBase):
    pass  # id_usuario se toma del token, no del body


class MascotaUpdate(BaseModel):
    nombre: Optional[str] = None
    especie: Optional[str] = None
    raza: Optional[str] = None
    sexo: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
    peso_kg: Optional[Decimal] = None
    color: Optional[str] = None
    esterilizado: Optional[bool] = None
    foto_url: Optional[str] = None


class MascotaOut(MascotaBase):
    model_config = ConfigDict(from_attributes=True)
    id_mascota: int
    id_usuario: int
    fecha_registro: Optional[datetime] = None
