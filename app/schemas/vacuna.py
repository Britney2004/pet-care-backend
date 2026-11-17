from datetime import date
from typing import Optional
from pydantic import BaseModel, ConfigDict


class VacunaBase(BaseModel):
    nombre_vacuna: str
    fecha_aplicacion: date
    fecha_proxima_dosis: Optional[date] = None
    id_veterinario: Optional[int] = None
    lote: Optional[str] = None


class VacunaCreate(VacunaBase):
    id_mascota: int


class VacunaUpdate(BaseModel):
    nombre_vacuna: Optional[str] = None
    fecha_aplicacion: Optional[date] = None
    fecha_proxima_dosis: Optional[date] = None
    id_veterinario: Optional[int] = None
    lote: Optional[str] = None


class VacunaOut(VacunaBase):
    model_config = ConfigDict(from_attributes=True)
    id_vacuna: int
    id_mascota: int
