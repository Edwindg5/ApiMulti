from fastapi import Request, HTTPException, Depends
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from app.utils.security import decode_access_token
from app.models.users import User
import jwt
import os
from dotenv import load_dotenv
from app.shared.config.db import get_db

# Cargar variables de entorno desde el archivo .env
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

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
