from pydantic import BaseModel, EmailStr, Field, field_validator,ConfigDict
from datetime import date
from typing import Literal, Optional

# ---------- User Schemas ----------
class UserCreate(BaseModel):
    username: str = Field(min_length=3)
    email: EmailStr
    password: str = Field(min_length=4)


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: str


class Token(BaseModel):
    access_token: str
    token_type: str


# ---------- Transaction Schemas ----------
class TransactionCreate(BaseModel):
    title: str
    amount: float = Field(gt=0)          # must be positive
    type: Literal["income", "expense"]
    category: str
    date: date


class TransactionUpdate(BaseModel):
    title: Optional[str] = None
    amount: Optional[float] = Field(default=None, gt=0)
    type: Optional[Literal["income", "expense"]] = None
    category: Optional[str] = None
    date: Optional[date] = None


class TransactionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    amount: float
    type: str
    category: str
    date: date
    owner_id: int