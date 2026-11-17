from datetime import date
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, ConfigDict


class HistorialBase(BaseModel):
    id_veterinario: Optional[int] = None
    id_cita: Optional[int] = None
    fecha: date
    diagnostico: Optional[str] = None
    tratamiento: Optional[str] = None
    peso_kg: Optional[Decimal] = None
    observaciones: Optional[str] = None


class HistorialCreate(HistorialBase):
    id_mascota: int


class HistorialUpdate(BaseModel):
    id_veterinario: Optional[int] = None
    fecha: Optional[date] = None
    diagnostico: Optional[str] = None
    tratamiento: Optional[str] = None
    peso_kg: Optional[Decimal] = None
    observaciones: Optional[str] = None


class HistorialOut(HistorialBase):
    model_config = ConfigDict(from_attributes=True)
    id_historial: int
    id_mascota: int
