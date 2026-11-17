from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.security import get_current_user, require_admin
from app.models.clinica import Clinica
from app.models.veterinario import Veterinario
from app.schemas.veterinario import VeterinarioCreate, VeterinarioUpdate, VeterinarioOut

router = APIRouter(prefix="/veterinarios", tags=["Veterinarios"], dependencies=[Depends(get_current_user)])


def _clinica_existe(db: Session, id_clinica: int):
    if not db.get(Clinica, id_clinica):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Clínica no encontrada")


@router.get("/", response_model=List[VeterinarioOut])
def listar(id_clinica: Optional[int] = None, especialidad: Optional[str] = None,
           skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    q = db.query(Veterinario)
    if id_clinica:
        q = q.filter(Veterinario.id_clinica == id_clinica)
    if especialidad:
        q = q.filter(Veterinario.especialidad.ilike(f"%{especialidad}%"))
    return q.order_by(Veterinario.apellido).offset(skip).limit(limit).all()


@router.get("/{id_veterinario}", response_model=VeterinarioOut)
def obtener(id_veterinario: int, db: Session = Depends(get_db)):
    v = db.get(Veterinario, id_veterinario)
    if not v:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Veterinario no encontrado")
    return v


@router.post("/", response_model=VeterinarioOut, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_admin)])
def crear(data: VeterinarioCreate, db: Session = Depends(get_db)):
    _clinica_existe(db, data.id_clinica)
    v = Veterinario(**data.model_dump())
    db.add(v); db.commit(); db.refresh(v)
    return v


@router.put("/{id_veterinario}", response_model=VeterinarioOut, dependencies=[Depends(require_admin)])
def actualizar(id_veterinario: int, data: VeterinarioUpdate, db: Session = Depends(get_db)):
    v = db.get(Veterinario, id_veterinario)
    if not v:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Veterinario no encontrado")
    cambios = data.model_dump(exclude_unset=True)
    if cambios.get("id_clinica") is not None:
        _clinica_existe(db, cambios["id_clinica"])
    for k, val in cambios.items():
        setattr(v, k, val)
    db.commit(); db.refresh(v)
    return v


@router.delete("/{id_veterinario}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_admin)])
def eliminar(id_veterinario: int, db: Session = Depends(get_db)):
    v = db.get(Veterinario, id_veterinario)
    if not v:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Veterinario no encontrado")
    db.delete(v); db.commit()
