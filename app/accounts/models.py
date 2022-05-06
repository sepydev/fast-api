from typing import Optional

from fastapi import HTTPException, status
from pydantic import EmailStr
from sqlmodel import SQLModel, Field, Column, VARCHAR
from sqlmodel import Session, select

from .dependencies import pwd_context


def get_password_hash(password):
    return pwd_context.hash(password)


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: EmailStr = Field(sa_column=Column("email", VARCHAR, unique=True, nullable=False))
    hashed_password: str
    is_active: bool = True

    class Objects:

        def create_user(session: Session, user: 'UserCreate', ):
            db_user = session.execute(select(User).where(User.email == user.email)).first()
            if db_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already exists",
                )
            if user.password != user.confirm_password:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Passwords and confirm passwords are not matched",
                )
            hashed_password = get_password_hash(user.password)
            db_user = User(email=user.email, hashed_password=hashed_password)
            if not db_user.email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email is not valid",
                )

            session.add(db_user)
            session.commit()
            session.refresh(db_user)
            return db_user

        def get_users(session: Session, offset: int = 0, limit: int = 100):
            users = session.execute(select(User).offset(offset).limit(limit)).scalars().all()
            return users

        def get_user(session: Session, user_id: int):
            user = session.get(User, user_id)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            return user

        def get_user_by_email(session: Session, email: str):
            db_user = session.exec(select(User).where(User.email == email)).first()
            return db_user


class UserOut(SQLModel):
    email: str = Field(title="Email")
    is_active: bool = Field(title="Is active")
    id: int = Field(title="id")


class UserCreate(SQLModel):
    email: EmailStr
    password: str
    confirm_password: str


class UserLogin(SQLModel):
    email: EmailStr
    password: str


class Token(SQLModel):
    access_token: str
    token_type: str


class TokenData(SQLModel):
    email: Optional[str] = None
