# Importamos todos los modelos para que SQLAlchemy resuelva las relaciones
# y Alembic detecte las tablas al autogenerar migraciones.
from app.models.usuario import Usuario
from app.models.clinica import Clinica
from app.models.veterinario import Veterinario
from app.models.mascota import Mascota
from app.models.cita import Cita
from app.models.historial_medico import HistorialMedico
from app.models.vacuna import Vacuna
