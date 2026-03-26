#1.importaciones
from fastapi import FastAPI
from app.routers import usuarios, varios
from app.data.db import engine
from app.data import usuario

usuario.Base.metadata.create_all(bind=engine)

app=FastAPI()

app=FastAPI(
    title='Mi primer API', 
    description="Diego Arvizu",
    version='1.0.0'
    )

app.include_router(usuarios.routerU)
app.include_router(varios.routerV)
