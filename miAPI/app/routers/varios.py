from typing import Optional
import asyncio 
from app.data.database import usuarios
from fastapi import APIRouter

routerV= APIRouter(
    tags=['Inicio']
)
#3.Endpoints
@routerV.get("/", tags=['Inicio'])
async def holaMundo():
    return {"mensaje":"Hola mundo FASTAPI"}

@routerV.get("v1/bienvenidos", tags=['Inicio'])
async def bien():
    return {"mensaje":"Bienvenidos"}    

@routerV.get("/v1/promedio", tags=['Inicio'])
async def promedio():
    await asyncio.sleep(3)   #simulación de peticion, consultaBD..
    return {
            "Claificacion":"8.5",
            "estatus":"200"
            }

@routerV.get("v1/usuario/{id}", tags=['Inicio'])
async def consultaUno(id:int):
    await asyncio.sleep(3)
    return {
        "Resultado":"Usuario encontrado",
        "estatus":"200"
        }

@routerV.get("/usuarios/", tags=['Inicio'])
async def consultaOp(id:Optional[int]=None):
    await asyncio.sleep(2)
    if id is not None:
        for usuario in usuarios:
            if usuario["id"]==str(id):
                return {"Usuario encontrado":id,"Datos":usuario}
        return {"Mensaje":"Usuario no encontrado"}
    else:
        return {"Aviso":"No se proporciono id"}