from datetime import date, timedelta
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.security import get_current_user
from app.crud.ownership import mascota_propia, validar_veterinario
from app.models.vacuna import Vacuna
from app.models.mascota import Mascota
from app.schemas.vacuna import VacunaCreate, VacunaUpdate, VacunaOut

router = APIRouter(prefix="/vacunas", tags=["Vacunas"])


def _vacuna_propia(db: Session, id_vacuna: int, user) -> Vacuna:
    v = (db.query(Vacuna).join(Mascota, Vacuna.id_mascota == Mascota.id_mascota)
         .filter(Vacuna.id_vacuna == id_vacuna, Mascota.id_usuario == user.id_usuario).first())
    if not v:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Vacuna no encontrada")
    return v


# OJO: esta ruta va ANTES de /{id_vacuna} para que "proximas" no se interprete como id
@router.get("/proximas", response_model=List[VacunaOut])
def proximas(dias: int = 30, db: Session = Depends(get_db), user=Depends(get_current_user)):
    """Refuerzos de todas mis mascotas que vencen en los próximos `dias` días."""
    hoy = date.today()
    return (db.query(Vacuna).join(Mascota, Vacuna.id_mascota == Mascota.id_mascota)
            .filter(Mascota.id_usuario == user.id_usuario,
                    Vacuna.fecha_proxima_dosis.isnot(None),
                    Vacuna.fecha_proxima_dosis.between(hoy, hoy + timedelta(days=dias)))
            .order_by(Vacuna.fecha_proxima_dosis).all())


@router.get("/mascota/{id_mascota}", response_model=List[VacunaOut])
def por_mascota(id_mascota: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    mascota_propia(db, id_mascota, user)
    return (db.query(Vacuna).filter(Vacuna.id_mascota == id_mascota)
            .order_by(Vacuna.fecha_aplicacion.desc()).all())


@router.get("/{id_vacuna}", response_model=VacunaOut)
def obtener(id_vacuna: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return _vacuna_propia(db, id_vacuna, user)


@router.post("/", response_model=VacunaOut, status_code=status.HTTP_201_CREATED)
def crear(data: VacunaCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    mascota_propia(db, data.id_mascota, user)
    validar_veterinario(db, data.id_veterinario)
    v = Vacuna(**data.model_dump())
    db.add(v); db.commit(); db.refresh(v)
    return v


@router.put("/{id_vacuna}", response_model=VacunaOut)
def actualizar(id_vacuna: int, data: VacunaUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    v = _vacuna_propia(db, id_vacuna, user)
    cambios = data.model_dump(exclude_unset=True)
    validar_veterinario(db, cambios.get("id_veterinario"))
    for k, val in cambios.items():
        setattr(v, k, val)
    db.commit(); db.refresh(v)
    return v


@router.delete("/{id_vacuna}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(id_vacuna: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    v = _vacuna_propia(db, id_vacuna, user)
    db.delete(v); db.commit()
