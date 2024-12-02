from fastapi import Request, HTTPException, Depends
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from app.utils.security import decode_access_token
from app.models.users import User
from fastapi import Depends, HTTPException, Security
from app.utils.security import hash_password
import jwt
import os
from dotenv import load_dotenv
from app.shared.config.db import get_db
from app.utils.security import decode_access_token
# Cargar variables de entorno desde el archivo .env
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")
def is_admin(token: str = Security(oauth2_scheme)):
    try:
        payload = decode_access_token(token)
        if payload.get("rol") != "ADMIN":
            raise HTTPException(status_code=403, detail="No tienes acceso a esta funcionalidad.")
    except Exception:
        raise HTTPException(status_code=403, detail="No tienes acceso.")

def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=401, detail="No se pudo validar las credenciales."
    )
    try:
        payload = decode_access_token(token)
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        user = db.query(User).filter(User.correo_electronico == email).first()
        if user is None:
            raise credentials_exception
        return user
    except Exception:
        raise credentials_exception
    



def create_admin_user(db: Session):
    admin_email = "admin@admin.com"
    admin_password = "admin123"
    existing_admin = db.query(User).filter(User.email == admin_email).first()

    if not existing_admin:
        admin = User(
            name="Administrador",
            email=admin_email,
            password=hash_password(admin_password),
            role="ADMIN",
        )
        db.add(admin)
        db.commit()
        print("Usuario ADMIN creado.")
    else:
        print("Usuario ADMIN ya existe.")



    

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Excluir rutas específicas de autenticación
        if request.url.path in ["/login", "/register"]:
            response = await call_next(request)
            return response

        # Validar encabezado de autorización
        token = request.headers.get("Authorization")
        if token is None:
            return JSONResponse(status_code=401, content={"detail": "Authorization header missing"})

        try:
            # Decodificar y verificar el token
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            request.state.user = payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")

        response = await call_next(request)
        return response
