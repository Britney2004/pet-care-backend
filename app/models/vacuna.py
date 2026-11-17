from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Vacuna(Base):
    __tablename__ = "vacunas"

    id_vacuna = Column(Integer, primary_key=True, index=True)
    id_mascota = Column(Integer, ForeignKey("mascotas.id_mascota", ondelete="CASCADE"), nullable=False, index=True)
    nombre_vacuna = Column(String(100), nullable=False)
    fecha_aplicacion = Column(Date, nullable=False)
    fecha_proxima_dosis = Column(Date)
    id_veterinario = Column(Integer, ForeignKey("veterinarios.id_veterinario", ondelete="SET NULL"))
    lote = Column(String(50))

    mascota = relationship("Mascota", back_populates="vacunas")
