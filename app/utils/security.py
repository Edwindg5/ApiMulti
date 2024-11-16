import jwt
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from enum import Enum

# Cargar variables de entorno desde el archivo .env
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")


# Enumeración para el estado de una transacción
from enum import Enum

# Enumeración para el estado general de la transacción
class TransactionStatus(str, Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    VENTA = "VENTA"
    INTERCAMBIO = "INTERCAMBIO"
    DONACIÓN = "DONACIÓN"
    DISPONIBLE = "DISPONIBLE"
    NO_DISPONIBLE = "NO_DISPONIBLE"
    ELIMINADO = "ELIMINADO"


# Enumeración para resultados de la transacción
class TransactionResult(str, Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class TransactionType(str, Enum):
    COMPRA = "compra"
    VENTA = "venta"
    INTERCAMBIO = "intercambio"
    PRESTAMO = "prestamo"

# Enumeración para roles de usuario
class UserRole(str, Enum):
    ADMIN = "ADMIN"
    USER = "USER"

# Función para crear un token de acceso
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=30)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt

# Función para decodificar un token de acceso
def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
