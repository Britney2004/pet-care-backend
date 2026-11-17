from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class Clinica(Base):
    __tablename__ = "clinicas"

    id_clinica = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), nullable=False)
    direccion = Column(String(200))
    telefono = Column(String(20))
    ciudad = Column(String(100), index=True)

    veterinarios = relationship("Veterinario", back_populates="clinica", cascade="all, delete-orphan")
