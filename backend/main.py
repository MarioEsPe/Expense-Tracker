# backend\main.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from . import models, schemas, crud, security
from .database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    """
    Función de dependencia para obtener una sesión de BD.
    Asegura que la sesión se cierre siempre, incluso si hay un error.
    """
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close() 

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@app.post("/auth/register", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Endpoint para registrar un nuevo usuario.
    """
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    return crud.create_user(db=db, user=user)


@app.post("/auth/login")
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    """
    Endpoint para iniciar sesión.
    Devuelve un Access Token (JWT) si las credenciales son válidas.
    """
    user = crud.get_user_by_email(db, email=form_data.username)

    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}, 
        )
    access_token = security.create_access_token(
        data={"sub": user.email}
    )

    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me", response_model=schemas.User)
def read_users_me(
    token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_db)
):
    """
    Un endpoint de ejemplo que requiere autenticación.
    (Lo implementaremos completamente más tarde).
    """
    user = crud.get_user_by_email(db, email="test@test.com")
    if user is None:
         raise HTTPException(status_code=404, detail="User not found")
    return user