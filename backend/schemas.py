# backend\schemas.py
from pydantic import BaseModel, EmailStr
from datetime import datetime, date
from decimal import Decimal

# --- Schemas para Expense ---

class ExpenseBase(BaseModel):
    amount: Decimal
    description: str | None = None
    expense_date: date
    category_id: int

class ExpenseCreate(ExpenseBase):
    pass # Para crear, necesitamos los mismos campos base

class Expense(ExpenseBase):
    id: int
    user_id: int
    created_at: datetime

    # Configuración para que Pydantic lea modelos de SQLAlchemy
    class Config:
        orm_mode = True

# --- Schemas para Category ---

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

# --- Schemas para User ---

class UserBase(BaseModel):
    email: EmailStr 

class UserCreate(UserBase):
    password: str 

class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True