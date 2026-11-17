from typing import Optional
from pydantic import BaseModel, ConfigDict


class VeterinarioBase(BaseModel):
    id_clinica: int
    nombre: str
    apellido: str
    especialidad: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None


class VeterinarioCreate(VeterinarioBase):
    pass


class VeterinarioUpdate(BaseModel):
    id_clinica: Optional[int] = None
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    especialidad: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None


class VeterinarioOut(VeterinarioBase):
    model_config = ConfigDict(from_attributes=True)
    id_veterinario: int
