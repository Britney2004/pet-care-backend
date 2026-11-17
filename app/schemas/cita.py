from datetime import datetime
from typing import Literal, Optional
from pydantic import BaseModel, ConfigDict

EstadoCita = Literal["pendiente", "confirmada", "cancelada", "completada"]


class CitaCreate(BaseModel):
    id_mascota: int
    id_veterinario: Optional[int] = None
    fecha_hora: datetime
    motivo: Optional[str] = None


class CitaUpdate(BaseModel):
    id_veterinario: Optional[int] = None
    fecha_hora: Optional[datetime] = None
    motivo: Optional[str] = None
    estado: Optional[EstadoCita] = None


class CitaOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id_cita: int
    id_mascota: int
    id_veterinario: Optional[int] = None
    fecha_hora: datetime
    motivo: Optional[str] = None
    estado: str
    fecha_creacion: Optional[datetime] = None
