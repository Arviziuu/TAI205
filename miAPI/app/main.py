#1. importaciones
from fastapi import FastAPI,status,HTTPException
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
    

@app.get("/v1/usuarios/", tags=['CRUD HTTP'])
async def consultaT():
    return{
        "status":"200",
        "total": len(usuarios),
        "data": usuarios
    }

@app.post("/v1/usuarios/", tags=['CRUD HTTP'])
async def crea_usuario(usuario:dict):
    for usr in usuarios:
        if usr["id"] == usuario.get("id"):
            raise HTTPException(
                status_code=400,
                detail="El id ya existe"
            )
    usuarios.append(usuario)
    return{
        "mensaje": "usuario agregado correctamente",
        "status":"200",
        "ususario":usuario
    }

@app.put("/v1/usuarios/{id}", tags=['CRUD HTTP'])
async def actualiza_usuario(id: int, usuario_actualizado: dict):
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios[index].update(usuario_actualizado)
            return {
                "mensaje": "Usuario actualizado correctamente",
                "status": "200",
                "usuario": usuarios[index]
            }
    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )

@app.delete("/v1/usuarios/{id}", tags=['CRUD HTTP'])
async def elimina_usuario(id: int):
    for usr in usuarios:
        if usr["id"] == id:
            usuarios.remove(usr)
            return {
                "mensaje": "Usuario eliminado correctamente",
                "status": "200"
            }
    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )


