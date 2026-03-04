# importaciones
from fastapi import FastAPI,status,HTTPException
from typing import Optional
import asyncio
from pydantic import BaseModel,Field, EmailStr
from datetime import datetime

# Inicialización APP
app=FastAPI(
    title='API Biblioteca Digital', 
    description="Diego Arvizu",
    version='1.0.0'
)

# BD ficticia
libros=[{"nombre":"Cien años de soledad","autor":"Gabriel García Márquez","año":1967,"paginas":471,"estado":"disponible"},
        {"nombre":"El principito","autor":"Antoine de Saint-Exupéry","año":1943,"paginas":96,"estado":"disponible"},
        {"nombre":"1984","autor":"George Orwell","año":1949,"paginas":328,"estado":"disponible"},
        {"nombre":"Don Quijote de la Mancha","autor":"Miguel de Cervantes","año":1605,"paginas":863,"estado":"disponible"}]

# Modelos
class crear_usuario(BaseModel):
    nombre: str = Field(min_length=2, max_length=100)
    correo: EmailStr 

class registar_libro(BaseModel):
    nombre: str = Field(min_length=2, max_length=100)
    autor: str = Field(min_length=2, max_length=100)
    año: int = Field(gt=1450, le=datetime.now().year)
    paginas: int = Field(gt=1)
    estado: str = Field(default="disponible", pattern="^(disponible|prestado)$")

# Registrar libro
@app.post("/v1/libros/", status_code=201, tags=['CRUD HTTP'])
async def registrar_libro(libro:registar_libro):
    for l in libros:
        if l["nombre"] == libro.nombre:
            raise HTTPException(
                status_code=400,
                detail="El libro ya existe"
            )
    libros.append(libro.model_dump())
    return{
        "mensaje": "Libro registrado correctamente",
        "libro":libro
    }

# Listar libros disponibles
@app.get("/v1/libros/", tags=['CRUD HTTP'])
async def listar_libros():
    disponibles = [l for l in libros if l["estado"] == "disponible"]
    return{
        "total": len(disponibles),
        "data": disponibles
    }

# Buscar libro por nombre
@app.get("/v1/libros/{nombre}", tags=['CRUD HTTP'])
async def buscar_libro(nombre:str):
    for libro in libros:
        if libro["nombre"] == nombre:
            return libro
    raise HTTPException(
        status_code=404,
        detail="Libro no encontrado"
    )

# Registrar préstamo
@app.put("/v1/libros/prestar/{nombre}", tags=['CRUD HTTP'])
async def prestar_libro(nombre:str, usuario: crear_usuario):
    for libro in libros:
        if libro["nombre"] == nombre:
            if libro["estado"] == "prestado":
                raise HTTPException(
                    status_code=409,
                    detail="Ya se registro el prestamo del libro"
                )
            libro["estado"] = "prestado"
            libro["usuario"] = usuario.model_dump()
            return{
                "mensaje":"Libro prestado correctamente"
            }
    raise HTTPException(
        status_code=404,
        detail="Libro no disponible"
    )

# Marcar libro como devuelto
@app.put("/v1/libros/devolver/{nombre}", tags=['CRUD HTTP'])
async def devolver_libro(nombre:str):
    for libro in libros:
        if libro["nombre"] == nombre:

            if libro["estado"] == "disponible":
                raise HTTPException(
                    status_code=409,
                    detail="El libro no está prestado"
                )
            libro["estado"] = "disponible"
            libro.pop("usuario", None)
            return{
                "mensaje":"Libro devuelto correctamente"
            }
    raise HTTPException(
        status_code=404,
        detail="Libro no encontrado"
    )

# Eliminar registro del préstamo
@app.delete("/v1/libros/prestamo/{nombre}", tags=['CRUD HTTP'])
async def eliminar_prestamo(nombre:str):
    for libro in libros:
        if libro["nombre"] == nombre:

            if libro["estado"] == "disponible":
                raise HTTPException(
                    status_code=409,
                    detail="El registro de préstamo no existe"
                )
            libro["estado"] = "disponible"
            libro.pop("usuario", None)

            return{
                "mensaje":"Registro de préstamo eliminado"
            }
    raise HTTPException(
        status_code=404,
        detail="Libro no encontrado"
    )