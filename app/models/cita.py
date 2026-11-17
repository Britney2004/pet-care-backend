from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base


class Cita(Base):
    __tablename__ = "citas"

    id_cita = Column(Integer, primary_key=True, index=True)
    id_mascota = Column(Integer, ForeignKey("mascotas.id_mascota", ondelete="CASCADE"), nullable=False, index=True)
    id_veterinario = Column(Integer, ForeignKey("veterinarios.id_veterinario", ondelete="SET NULL"), index=True)
    fecha_hora = Column(DateTime, nullable=False)
    motivo = Column(String(255))
    estado = Column(String(20), nullable=False, default="pendiente")
    fecha_creacion = Column(DateTime, server_default=func.now())

    mascota = relationship("Mascota", back_populates="citas")
    veterinario = relationship("Veterinario")
