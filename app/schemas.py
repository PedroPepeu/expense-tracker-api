from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from .models import CategoryEnum


class UserCreate(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True


class ExpenseBase(BaseModel):
    amount: float
    category: CategoryEnum
    description: Optional[str] = None
    date: datetime = datetime.now()


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseOut(ExpenseBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
