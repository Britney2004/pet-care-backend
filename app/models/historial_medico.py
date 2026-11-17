from sqlalchemy import Column, Integer, Date, Numeric, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class HistorialMedico(Base):
    __tablename__ = "historial_medico"

    id_historial = Column(Integer, primary_key=True, index=True)
    id_mascota = Column(Integer, ForeignKey("mascotas.id_mascota", ondelete="CASCADE"), nullable=False, index=True)
    id_veterinario = Column(Integer, ForeignKey("veterinarios.id_veterinario", ondelete="SET NULL"))
    id_cita = Column(Integer, ForeignKey("citas.id_cita", ondelete="SET NULL"))
    fecha = Column(Date, nullable=False)
    diagnostico = Column(Text)
    tratamiento = Column(Text)
    peso_kg = Column(Numeric(5, 2))
    observaciones = Column(Text)

    mascota = relationship("Mascota", back_populates="historial")
