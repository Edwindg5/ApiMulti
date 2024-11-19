import jwt
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from enum import Enum
from passlib.context import CryptContext  # Manejo de contraseñas

# Cargar variables de entorno desde el archivo .env
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

# Configuración para hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Enumeración para el estado de una transacción
class TransactionStatus(str, Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    VENTA = "VENTA"
    INTERCAMBIO = "INTERCAMBIO"
    DONACION = "DONACION"
    DISPONIBLE = "DISPONIBLE"
    NO_DISPONIBLE = "NO_DISPONIBLE"
    ELIMINADO = "ELIMINADO"

# Enumeración para resultados de la transacción
class TransactionResult(str, Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

# Enumeración para tipos de transacción
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
    """Crea un token JWT con datos codificados y tiempo de expiración."""
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt

# Función para decodificar un token de acceso
def decode_access_token(token: str):
    """Decodifica un token JWT y valida su firma y expiración."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

# Función para hashear contraseñas
def hash_password(password: str) -> str:
    """Hashea una contraseña utilizando bcrypt."""
    return pwd_context.hash(password)

# Función para verificar contraseñas
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si una contraseña en texto plano coincide con un hash."""
    return pwd_context.verify(plain_password, hashed_password)
