from typing import Optional

from sqlmodel import SQLModel, Field, Column, VARCHAR
from pydantic import EmailStr, BaseModel, Field as F


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: EmailStr = Field(sa_column=Column("email", VARCHAR, unique=True, nullable=False))
    hashed_password: str
    is_active: bool = True


class UserOut(BaseModel):
    email: str = F(title="Email")
    is_active: bool = F(title="Is active")
    id: int = F(title="id")


class UserCreate(SQLModel):
    email: EmailStr
    password: str
    confirm_password: str
