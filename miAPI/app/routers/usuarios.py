from fastapi import status,HTTPException,Depends, APIRouter
from app.data.database import usuarios
from app.models.usuarios import crear_usuario
from app.security.auth import verificar_peticion

routerU= APIRouter(
    prefix="/v1/usuarios",
    tags=['CRUD HTTP']
)

@routerU.get("/")
async def consulta():
    return{
        "status":"200",
        "total":len(usuarios),
        "data": usuarios
    }

@routerU.post("/", status_code=status.HTTP_201_CREATED)
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

@routerU.put("/{id}")
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

@routerU.delete("/{id}")
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