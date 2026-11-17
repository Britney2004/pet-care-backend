from sqlalchemy import Column, Integer, String, Date, Numeric, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base


class Mascota(Base):
    __tablename__ = "mascotas"

    id_mascota = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario", ondelete="CASCADE"), nullable=False, index=True)
    nombre = Column(String(100), nullable=False)
    especie = Column(String(50), nullable=False)
    raza = Column(String(100))
    sexo = Column(String(10))
    fecha_nacimiento = Column(Date)
    peso_kg = Column(Numeric(5, 2))
    color = Column(String(50))
    esterilizado = Column(Boolean, default=False)
    foto_url = Column(String(255))
    fecha_registro = Column(DateTime, server_default=func.now())

    citas = relationship("Cita", back_populates="mascota", cascade="all, delete-orphan")
    historial = relationship("HistorialMedico", back_populates="mascota", cascade="all, delete-orphan")
    vacunas = relationship("Vacuna", back_populates="mascota", cascade="all, delete-orphan")
