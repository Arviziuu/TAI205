from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta

app = FastAPI()

# CONFIGURACIÓN JWT
SECRET_KEY = "mi_clave_secreta"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

#BASE DE DATOS FICTICIA
fake_users_db = {
    "diego": {
        "username": "diego",
        "password": "1234"
    },
    "admin": {
        "username": "admin",
        "password": "admin123"
    }
}

# OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

#FUNCIÓN PARA OBTENER USUARIO
def get_user(username: str):
    return fake_users_db.get(username)

#CREAR TOKEN
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

#VALIDAR TOKEN
def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")

        user = get_user(username)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario no válido"
            )

        return user

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado"
        )

#LOGIN (GENERA TOKEN)
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user(form_data.username)

    if not user or user["password"] != form_data.password:
        raise HTTPException(
            status_code=400,
            detail="Credenciales incorrectas"
        )

    access_token = create_access_token(data={"sub": user["username"]})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

#ENDPOINT PÚBLICO
@app.get("/")
def public():
    return {"mensaje": "Endpoint público"}

#ENDPOINT PROTEGIDO (PUT)
@app.put("/protegido")
def protegido_put(user: dict = Depends(verify_token)):
    return {
        "mensaje": f"Acceso autorizado PUT",
        "usuario": user["username"]
    }

#ENDPOINT PROTEGIDO (DELETE)
@app.delete("/protegido")
def protegido_delete(user: dict = Depends(verify_token)):
    return {
        "mensaje": f"Acceso autorizado DELETE",
        "usuario": user["username"]
    }