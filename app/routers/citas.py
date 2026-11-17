from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.security import get_current_user
from app.crud.ownership import mascota_propia, validar_veterinario
from app.models.cita import Cita
from app.models.mascota import Mascota
from app.schemas.cita import CitaCreate, CitaUpdate, CitaOut, EstadoCita

router = APIRouter(prefix="/citas", tags=["Citas"])


def _cita_propia(db: Session, id_cita: int, user) -> Cita:
    c = (db.query(Cita).join(Mascota, Cita.id_mascota == Mascota.id_mascota)
         .filter(Cita.id_cita == id_cita, Mascota.id_usuario == user.id_usuario).first())
    if not c:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Cita no encontrada")
    return c


@router.get("/", response_model=List[CitaOut])
def listar(id_mascota: Optional[int] = None, estado: Optional[EstadoCita] = None,
           db: Session = Depends(get_db), user=Depends(get_current_user)):
    q = (db.query(Cita).join(Mascota, Cita.id_mascota == Mascota.id_mascota)
         .filter(Mascota.id_usuario == user.id_usuario))
    if id_mascota:
        q = q.filter(Cita.id_mascota == id_mascota)
    if estado:
        q = q.filter(Cita.estado == estado)
    return q.order_by(Cita.fecha_hora).all()


@router.get("/{id_cita}", response_model=CitaOut)
def obtener(id_cita: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return _cita_propia(db, id_cita, user)


@router.post("/", response_model=CitaOut, status_code=status.HTTP_201_CREATED)
def crear(data: CitaCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    mascota_propia(db, data.id_mascota, user)
    validar_veterinario(db, data.id_veterinario)
    c = Cita(**data.model_dump(), estado="pendiente")
    db.add(c); db.commit(); db.refresh(c)
    return c


@router.put("/{id_cita}", response_model=CitaOut)
def actualizar(id_cita: int, data: CitaUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    c = _cita_propia(db, id_cita, user)
    cambios = data.model_dump(exclude_unset=True)
    validar_veterinario(db, cambios.get("id_veterinario"))
    for k, v in cambios.items():
        setattr(c, k, v)
    db.commit(); db.refresh(c)
    return c


@router.patch("/{id_cita}/cancelar", response_model=CitaOut)
def cancelar(id_cita: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    c = _cita_propia(db, id_cita, user)
    c.estado = "cancelada"
    db.commit(); db.refresh(c)
    return c


@router.delete("/{id_cita}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(id_cita: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    c = _cita_propia(db, id_cita, user)
    db.delete(c); db.commit()
