from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.security import get_current_user, require_admin
from app.models.clinica import Clinica
from app.schemas.clinica import ClinicaCreate, ClinicaUpdate, ClinicaOut

router = APIRouter(prefix="/clinicas", tags=["Clínicas"], dependencies=[Depends(get_current_user)])


@router.get("/", response_model=List[ClinicaOut])
def listar(ciudad: Optional[str] = None, skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    q = db.query(Clinica)
    if ciudad:
        q = q.filter(Clinica.ciudad.ilike(f"%{ciudad}%"))
    return q.order_by(Clinica.nombre).offset(skip).limit(limit).all()


@router.get("/{id_clinica}", response_model=ClinicaOut)
def obtener(id_clinica: int, db: Session = Depends(get_db)):
    c = db.get(Clinica, id_clinica)
    if not c:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Clínica no encontrada")
    return c


@router.post("/", response_model=ClinicaOut, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_admin)])
def crear(data: ClinicaCreate, db: Session = Depends(get_db)):
    c = Clinica(**data.model_dump())
    db.add(c); db.commit(); db.refresh(c)
    return c


@router.put("/{id_clinica}", response_model=ClinicaOut, dependencies=[Depends(require_admin)])
def actualizar(id_clinica: int, data: ClinicaUpdate, db: Session = Depends(get_db)):
    c = db.get(Clinica, id_clinica)
    if not c:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Clínica no encontrada")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(c, k, v)
    db.commit(); db.refresh(c)
    return c


@router.delete("/{id_clinica}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_admin)])
def eliminar(id_clinica: int, db: Session = Depends(get_db)):
    c = db.get(Clinica, id_clinica)
    if not c:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Clínica no encontrada")
    db.delete(c); db.commit()
