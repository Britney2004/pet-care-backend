from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.security import get_current_user
from app.crud.ownership import mascota_propia, validar_veterinario, validar_cita_de_mascota
from app.models.historial_medico import HistorialMedico
from app.models.mascota import Mascota
from app.schemas.historial_medico import HistorialCreate, HistorialUpdate, HistorialOut

router = APIRouter(prefix="/historial", tags=["Historial médico"])


def _registro_propio(db: Session, id_historial: int, user) -> HistorialMedico:
    h = (db.query(HistorialMedico).join(Mascota, HistorialMedico.id_mascota == Mascota.id_mascota)
         .filter(HistorialMedico.id_historial == id_historial, Mascota.id_usuario == user.id_usuario).first())
    if not h:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Registro no encontrado")
    return h


@router.get("/mascota/{id_mascota}", response_model=List[HistorialOut])
def por_mascota(id_mascota: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    mascota_propia(db, id_mascota, user)
    return (db.query(HistorialMedico).filter(HistorialMedico.id_mascota == id_mascota)
            .order_by(HistorialMedico.fecha.desc()).all())


@router.get("/{id_historial}", response_model=HistorialOut)
def obtener(id_historial: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return _registro_propio(db, id_historial, user)


@router.post("/", response_model=HistorialOut, status_code=status.HTTP_201_CREATED)
def crear(data: HistorialCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    mascota_propia(db, data.id_mascota, user)
    validar_veterinario(db, data.id_veterinario)
    validar_cita_de_mascota(db, data.id_cita, data.id_mascota)
    h = HistorialMedico(**data.model_dump())
    db.add(h); db.commit(); db.refresh(h)
    return h


@router.put("/{id_historial}", response_model=HistorialOut)
def actualizar(id_historial: int, data: HistorialUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    h = _registro_propio(db, id_historial, user)
    cambios = data.model_dump(exclude_unset=True)
    validar_veterinario(db, cambios.get("id_veterinario"))
    for k, v in cambios.items():
        setattr(h, k, v)
    db.commit(); db.refresh(h)
    return h


@router.delete("/{id_historial}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(id_historial: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    h = _registro_propio(db, id_historial, user)
    db.delete(h); db.commit()
