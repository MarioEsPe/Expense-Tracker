# backend\crud.py
from sqlalchemy.orm import Session

from . import models, schemas
from . import security 

# --- Funciones CRUD para User ---

def get_user_by_email(db: Session, email: str) -> models.User | None:
    """
    Busca y devuelve un usuario por su email.
    Devuelve None si no se encuentra.
    """
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """
    Crea un nuevo usuario en la base de datos.
    """
    hashed_password = security.hash_password(user.password)

    db_user = models.User(
        email=user.email, 
        hashed_password=hashed_password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user