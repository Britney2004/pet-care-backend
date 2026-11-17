from typing import Optional
from pydantic import BaseModel, ConfigDict


class ClinicaBase(BaseModel):
    nombre: str
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    ciudad: Optional[str] = None


class ClinicaCreate(ClinicaBase):
    pass


class ClinicaUpdate(BaseModel):
    nombre: Optional[str] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    ciudad: Optional[str] = None


class ClinicaOut(ClinicaBase):
    model_config = ConfigDict(from_attributes=True)
    id_clinica: int
