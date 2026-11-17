from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.security import get_current_user
from app.crud.ownership import mascota_propia
from app.models.mascota import Mascota
from app.schemas.mascota import MascotaCreate, MascotaUpdate, MascotaOut

router = APIRouter(prefix="/mascotas", tags=["Mascotas"])


@router.get("/", response_model=List[MascotaOut])
def mis_mascotas(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(Mascota).filter(Mascota.id_usuario == user.id_usuario).order_by(Mascota.nombre).all()


@router.get("/{id_mascota}", response_model=MascotaOut)
def obtener(id_mascota: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return mascota_propia(db, id_mascota, user)


@router.post("/", response_model=MascotaOut, status_code=status.HTTP_201_CREATED)
def crear(data: MascotaCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    m = Mascota(**data.model_dump(), id_usuario=user.id_usuario)
    db.add(m); db.commit(); db.refresh(m)
    return m


@router.put("/{id_mascota}", response_model=MascotaOut)
def actualizar(id_mascota: int, data: MascotaUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    m = mascota_propia(db, id_mascota, user)
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(m, k, v)
    db.commit(); db.refresh(m)
    return m


@router.delete("/{id_mascota}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(id_mascota: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    m = mascota_propia(db, id_mascota, user)
    db.delete(m); db.commit()
