from datetime import datetime
from fastapi import FastAPI, status, HTTPException, Depends
from typing import Optional
from pydantic import BaseModel, Field
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

app = FastAPI(
    title="Api Examen 2do Parcial",
    description="Diego Arvizu",
    version="1.0.0"
)

# BD ficticia
reservas = [
    {"id": 1, "nombre": "Diego", "fecha_entrada": "09-03-2026", "fecha_salida": "15-03-2026", "habitacion": "sencilla", "tiempo_estancia": 6},
    {"id": 2, "nombre": "Osiel", "fecha_entrada": "09-03-2026", "fecha_salida": "15-03-2026", "habitacion": "doble", "tiempo_estancia": 6},
    {"id": 3, "nombre": "Ivan", "fecha_entrada": "09-03-2026", "fecha_salida": "15-03-2026", "habitacion": "suite", "tiempo_estancia": 6}
]

class CrearReserva(BaseModel):
    id: int = Field(..., gt=0, description="Identificador de reserva")
    nombre: str = Field(..., min_length=3, max_length=50, example="Diego")
    fecha_entrada: str = Field(..., example="09-03-2026")
    fecha_salida: str = Field(..., example="15-03-2026")
    habitacion: str = Field(..., example="sencilla")
    tiempo_estancia: int = Field(..., gt=0, description="Duración de la estancia en días")

seguridad = HTTPBasic()

def verificar_peticion(credenciales: HTTPBasicCredentials = Depends(seguridad)):
    userAuth = secrets.compare_digest(credenciales.username, "hotel")
    passAuth = secrets.compare_digest(credenciales.password, "r2026")
    if not (userAuth and passAuth):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales no autorizadas"
        )
    return credenciales.username

# Crear reserva
@app.post("/v1/reservas", status_code=status.HTTP_201_CREATED, tags=['CRUD HTTP'])
async def crear_reserva(reserva: CrearReserva, usuario: str = Depends(verificar_peticion)):

    for r in reservas:
        if r["id"] == reserva.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe reserva con este ID"
            )
    nueva_reserva = {
        "id": reserva.id,
        "nombre": reserva.nombre,
        "fecha_entrada": reserva.fecha_entrada,
        "fecha_salida": reserva.fecha_salida,
        "habitacion": reserva.habitacion,
        "tiempo_estancia": reserva.tiempo_estancia
    }
    reservas.append(nueva_reserva)
    return {
        "mensaje": "Reserva creada exitosamente",
        "reserva": nueva_reserva
    }

# Listar reservas
@app.get("/v1/reservas/", tags=['CRUD HTTP'])
async def listar_reservas():
    return {
        "total": len(reservas),
        "data": reservas
    }

# Consultar por ID
@app.get("/v1/reservas/id", tags=['CRUD HTTP'])
async def consultar_reserva(id: int):
    for reserva in reservas:
        if reserva["id"] == id:
            return reserva

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Reserva no encontrada"
    )

# Confirmar reserva
@app.put("/v1/reservas/id/confirmar", tags=['CRUD HTTP'])
async def confirmar_reserva(id: int):
    for reserva in reservas:
        if reserva["id"] == id:
            reserva["confirmada"] = True
            return {
                "mensaje": "Reserva confirmada exitosamente",
                "reserva": reserva
            }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Reserva no encontrada"
    )

# Cancelar reserva
@app.delete("/v1/reservas/id/cancelar", tags=['CRUD HTTP'])
async def cancelar_reserva(id: int):
    for reserva in reservas:
        if reserva["id"] == id:
            reservas.remove(reserva)
            return {"mensaje": "Reserva cancelada exitosamente"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Reserva no encontrada"
    )