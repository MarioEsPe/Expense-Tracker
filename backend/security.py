# backend\security.py
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from pydantic import BaseModel

# --- 1. Configuración de Hashing (Passlib) ---

# Definimos el contexto de hashing. Usaremos bcrypt.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Función para "hashear" una contraseña
def hash_password(password: str) -> str:
    """Toma una contraseña en texto plano y devuelve su hash."""
    return pwd_context.hash(password)

# Función para verificar una contraseña
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Compara una contraseña en texto plano con un hash."""
    return pwd_context.verify(plain_password, hashed_password)


# --- 2. Configuración de Tokens (JWT) ---

# ¡CRÍTICO DE SEGURIDAD!
# Esta es tu "llave secreta". NUNCA la compartas ni la subas a GitHub
# en un proyecto real. Se carga desde una variable de entorno.
# Puedes generar una tú mismo en la terminal con: openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # El token será válido por 30 minutos

# Función para crear un nuevo Access Token (JWT)
def create_access_token(data: dict) -> str:
    """
    Toma un diccionario de datos (payload) y crea un JWT.
    El 'sub' (subject) del token debe ser el 'email' o 'id' del usuario.
    """
    to_encode = data.copy()

    # Añade el tiempo de expiración al token (en UTC)
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    # Codifica el token con nuestra llave secreta y algoritmo
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Modelo Pydantic para el payload del token
# Esto nos ayudará a validar el contenido del token cuando lo decodifiquemos
class TokenData(BaseModel):
    email: str | None = None