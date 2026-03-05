#1.importaciones
from fastapi import FastAPI,status,HTTPException,Depends
from typing import Optional
import asyncio
from pydantic import BaseModel, Field   #Agregar BaseModel pydantic
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

#2. Inicialización APP
app = FastAPI()

#3. Endpoints
app=FastAPI(
    title='Mi primer API', 
    description="Ivan Moreno",
    version='1.0.0'
    )


#BD ficticia
usuarios=[
    {"id":1,"nombre":"Diego","edad":38},
    {"id":2,"nombre":"Dafne","edad":20},
    {"id":3,"nombre":"Ana","edad":20}
]

#Modelo de validación pydantic   ---creamos el modelo
class crear_usuario(BaseModel):
    id: int = Field (...,gt=0, description="Identificador de usuario")
    nombre: str= Field(..., min_length=3, max_length=50, example="Elizabeth")
    edad: int= Field(...,ge=1, le=123, description="Edad valida de 1 y 123")

#seguridad HTTP BASIC
seguridad=HTTPBasic()

def verificar_peticion(credenciales:HTTPBasicCredentials=Depends(seguridad)):
    userAuth=secrets.compare_digest(credenciales.username,"diego")
    passAuth=secrets.compare_digest(credenciales.password,"123456")

    if not (userAuth and passAuth):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales no autorizadas"
            )
    return credenciales.username
    

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
            "Claificacion":"8.5",
            "estatus":"200"
            }

@app.get("v1/usuario/{id}", tags=['Parametros'])
async def consultaUno(id:int):
    await asyncio.sleep(3)
    return {
        "Resultado":"Usuario encontrado",
        "estatus":"200"
        }

@app.get("/v1/usuarios/", tags=['Parametro Opcional'])
async def consultaOp(id:Optional[int]=None):
    await asyncio.sleep(2)
    if id is not None:
        for usuario in usuarios:
            if usuario["id"]==str(id):
                return {"Usuario encontrado":id,"Datos":usuario}
        return {"Mensaje":"Usuario no encontrado"}
    else:
        return {"Aviso":"No se proporciono id"}


@app.get("/v1/usuario/", tags=['CRUD HTTP'])
async def consulta():
    return{
        "status":"200",
        "total":len(usuarios),
        "data": usuarios
    }

@app.post("/v1/usuario/", tags=['CRUD HTTP'], status_code=status.HTTP_201_CREATED)
async def crea_usuario(usuario: crear_usuario): #---- usamos el modelo
    for usr in usuarios:
        if usr["id"] == usuario.id: #----cambiamos por que ya no usamos dict
            raise HTTPException(
                status_code=400, 
                detail= "El id ya existe"
            )
    usuarios.append(usuario)
    return{
        "mensaje":"Usuario agregado correctamente",
        "usuario":usuario
    }

@app.put("/v1/usuario/{id}", tags=['CRUD HTTP'])
async def actualizar_usuario(id: int, usuario_actualizado: dict):

    for i, usuario in enumerate(usuarios):
        if usuario["id"] == str(id):

            usuarios[i]["nombre"] = usuario_actualizado.get("nombre", usuario["nombre"])
            usuarios[i]["edad"] = usuario_actualizado.get("edad", usuario["edad"])

            return {
                "mensaje": "Usuario actualizado correctamente",
                "status": "200",
                "usuario": usuarios[i]
            }

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )

@app.delete("/v1/usuario/{id}", tags=['CRUD HTTP'])
async def eliminar_usuario(id: int, userAuth:str=Depends(verificar_peticion)):

    for i, usuario in enumerate(usuarios):
        if usuario["id"] == id:

            usuario_eliminado = usuarios.pop(i)

            return {
                "mensaje": f"Usuario eliminado por {userAuth}",
                "status": "200",
                "usuario": usuario_eliminado
            }

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )