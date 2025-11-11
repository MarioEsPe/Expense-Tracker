# backend\main.py
from fastapi import FastAPI
from .import models  # Importamos nuestros modelos
from . database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

# --- Instancia de la Aplicación FastAPI ---
app = FastAPI()

# --- Endpoint de Prueba ---
@app.get("/")
def read_root():
    return {"message": "Welcome to the Expense Tracker API v1"}