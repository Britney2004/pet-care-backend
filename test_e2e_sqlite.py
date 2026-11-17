import os, sys
os.environ.update(POSTGRES_USER="x", POSTGRES_PASSWORD="x", POSTGRES_DB="x", POSTGRES_HOST="x", POSTGRES_PORT="1",
    DATABASE_URL="sqlite:////tmp/test.db", SECRET_KEY="k", ALGORITHM="HS256", ACCESS_TOKEN_EXPIRE_MINUTES="60")
if os.path.exists("/tmp/test.db"): os.remove("/tmp/test.db")
sys.path.insert(0, ".")
from fastapi.testclient import TestClient
from app.main import app as fastapi_app
from app.database import Base, engine, SessionLocal
import app.models as _m
from app.models.usuario import Usuario
Base.metadata.create_all(engine)
c = TestClient(fastapi_app)

def registrar(n, mail):
    r = c.post("/auth/register", json={"nombre_completo": n, "correo_electronico": mail, "contrasena": "Clave123"}); assert r.status_code == 201, r.text
    t = c.post("/auth/login", data={"username": mail, "password": "Clave123"}).json()["access_token"]
    return {"Authorization": f"Bearer {t}"}

A = registrar("Ana", "ana@test.com"); B = registrar("Beto", "beto@test.com")
# hacer admin a Ana
db = SessionLocal(); db.query(Usuario).filter_by(correo_electronico="ana@test.com").update({"rol": "admin"}); db.commit(); db.close()

# permisos clínicas
assert c.post("/clinicas/", json={"nombre": "X"}, headers=B).status_code == 403
r = c.post("/clinicas/", json={"nombre": "VetSuba", "ciudad": "Bogotá"}, headers=A); assert r.status_code == 201, r.text; cid = r.json()["id_clinica"]
assert len(c.get("/clinicas/?ciudad=bogo", headers=B).json()) == 1
r = c.post("/veterinarios/", json={"id_clinica": cid, "nombre": "Luis", "apellido": "Paz", "especialidad": "Felinos"}, headers=A); assert r.status_code == 201, r.text; vid = r.json()["id_veterinario"]
assert c.post("/veterinarios/", json={"id_clinica": 999, "nombre": "a", "apellido": "b"}, headers=A).status_code == 404

# mascotas + aislamiento
r = c.post("/mascotas/", json={"nombre": "Firulais", "especie": "Perro", "peso_kg": "12.5"}, headers=B); assert r.status_code == 201, r.text; mid = r.json()["id_mascota"]
assert c.get(f"/mascotas/{mid}", headers=A).status_code == 404
assert c.get("/mascotas/", headers=A).json() == []

# citas
r = c.post("/citas/", json={"id_mascota": mid, "id_veterinario": vid, "fecha_hora": "2026-10-05T10:00:00", "motivo": "Control"}, headers=B); assert r.status_code == 201, r.text; ci = r.json()["id_cita"]
assert c.post("/citas/", json={"id_mascota": mid, "fecha_hora": "2026-10-05T10:00:00"}, headers=A).status_code == 404
assert c.patch(f"/citas/{ci}/cancelar", headers=B).json()["estado"] == "cancelada"
assert c.put(f"/citas/{ci}", json={"estado": "inventado"}, headers=B).status_code == 422

# historial
r = c.post("/historial/", json={"id_mascota": mid, "id_cita": ci, "id_veterinario": vid, "fecha": "2026-10-05", "diagnostico": "Sano"}, headers=B); assert r.status_code == 201, r.text
assert len(c.get(f"/historial/mascota/{mid}", headers=B).json()) == 1
assert c.get(f"/historial/mascota/{mid}", headers=A).status_code == 404

# vacunas
from datetime import date, timedelta
prox = (date.today() + timedelta(days=10)).isoformat()
r = c.post("/vacunas/", json={"id_mascota": mid, "nombre_vacuna": "Rabia", "fecha_aplicacion": "2026-09-01", "fecha_proxima_dosis": prox}, headers=B); assert r.status_code == 201, r.text
assert len(c.get("/vacunas/proximas?dias=30", headers=B).json()) == 1
assert len(c.get(f"/vacunas/mascota/{mid}", headers=B).json()) == 1

# borrar mascota (cascada)
assert c.delete(f"/mascotas/{mid}", headers=B).status_code == 204
assert c.get(f"/historial/mascota/{mid}", headers=B).status_code == 404
print("TODO OK")
