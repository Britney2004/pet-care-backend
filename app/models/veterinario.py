from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Veterinario(Base):
    __tablename__ = "veterinarios"

    id_veterinario = Column(Integer, primary_key=True, index=True)
    id_clinica = Column(Integer, ForeignKey("clinicas.id_clinica", ondelete="CASCADE"), nullable=False, index=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    especialidad = Column(String(100))
    telefono = Column(String(20))
    email = Column(String(150))

    clinica = relationship("Clinica", back_populates="veterinarios")
