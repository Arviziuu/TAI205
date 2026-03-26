from fastapi import status,HTTPException,Depends, APIRouter
from app.data.database import usuarios
from app.models.usuarios import crear_usuario
from app.security.auth import verificar_peticion

from sqlalchemy.orm import Session
from app.data.db import get_db
from app.data.usuario import usuario as usuarioDB

routerU= APIRouter(
    prefix="/v1/usuarios",
    tags=['CRUD HTTP']
)

@routerU.get("/")
async def consulta(db:Session = Depends(get_db)):
    queryUsuarios= db.query(usuarioDB).all()

    return{
        "status":"200",
        "total":len(queryUsuarios),
        "data": queryUsuarios
    }

@routerU.post("/", status_code=status.HTTP_201_CREATED)
async def crea_usuario(usuarioP: crear_usuario, db:Session = Depends(get_db)): #---- usamos el modelo
    usuarioNuevo= usuarioDB(nombre=usuarioP.nombre, edad=usuarioP.edad)

    db.add(usuarioNuevo)
    db.commit()
    db.refresh(usuarioNuevo)

    return{
        "mensaje":"Usuario agregado correctamente",
        "usuario":usuarioP
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