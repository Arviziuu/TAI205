#1. importaciones
from fastapi import FastAPI
from typing import Optional
import asyncio

#2.Inicialización APP
app=FastAPI(
    title='Mi primer API', 
    description="Diego Arvizu",
    version='1.0.0'
    )


#BD ficticia
usuarios=[
    {"id":1,"nombre":"Ivan","edad":"38"},
    {"id":2,"nombre":"Diana","edad":"20"},
    {"id":3,"nombre":"Julain","edad":"20"}
]

#3.Endpoints
@app.get("/", tags=['Inicio'])
async def holaMundo():
    return {"mensaje":"Hola mundo FASTAPI"}

@app.get("v1/bienvenidos", tags=['Inicio'])
async def bien():
    return {"mensaje":"Bienvenidos"}    

@app.get("/v1/promedio", tags=['Calificaciones'])
async def promedio():
    await asyncio.sleep(3)   #simulación de peticion, consultaBD..
    return {
             "Claificacion":"7.5",
             "estatus":"200"
             }

@app.get("/v1/usuario/{id}", tags=['Parametros'])
async def consultaUno(id:int):
    await asyncio.sleep(3)
    return {
        "Resultado":"Usuario encontrado",
        "estatus":"200"
        }  

@app.get("/v1/usuarios_op/", tags=['Parametro opcional'])
async def consultaOp(id:Optional[int]=None):
    await asyncio.sleep(2)
    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id:
                return {"Usuario encontrado":id,"Datos":usuario }
        return { "Mensaje":"usuario no encontrado" }
    else:
        return { "Aviso":"No se proporciono Id"}