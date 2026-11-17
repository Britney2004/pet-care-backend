from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.mascota import Mascota
from app.models.veterinario import Veterinario
from app.models.cita import Cita


def mascota_propia(db: Session, id_mascota: int, user) -> Mascota:
    """Devuelve la mascota solo si pertenece al usuario autenticado (si no, 404)."""
    m = db.query(Mascota).filter(
        Mascota.id_mascota == id_mascota, Mascota.id_usuario == user.id_usuario
    ).first()
    if not m:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Mascota no encontrada")
    return m


def validar_veterinario(db: Session, id_veterinario):
    if id_veterinario is not None and not db.get(Veterinario, id_veterinario):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Veterinario no encontrado")


def validar_cita_de_mascota(db: Session, id_cita, id_mascota: int):
    if id_cita is None:
        return
    c = db.get(Cita, id_cita)
    if not c or c.id_mascota != id_mascota:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "La cita no existe o no pertenece a esa mascota")
