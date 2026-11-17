from fastapi import FastAPI

from app.routers import auth, usuarios, clinicas, veterinarios, mascotas, citas, historial, vacunas

app = FastAPI(
    title="PeludOS API",
    description="API para la plataforma de cuidado de mascotas",
    version="0.1.0",
)

app.include_router(auth.router)
app.include_router(usuarios.router)
app.include_router(clinicas.router)
app.include_router(veterinarios.router)
app.include_router(mascotas.router)
app.include_router(citas.router)
app.include_router(historial.router)
app.include_router(vacunas.router)


@app.get("/health", tags=["Salud"])
def health_check():
    """
    Endpoint simple para verificar que la API está corriendo
    y respondiendo correctamente.
    """
    return {"status": "ok", "app": "PeludOS API"}