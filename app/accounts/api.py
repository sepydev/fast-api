from datetime import timedelta

from database import get_session
from fastapi import APIRouter, Depends, HTTPException, status
from settings import ACCESS_TOKEN_EXPIRE_MINUTES
from sqlmodel import Session

from . import auth
from .models import User, UserCreate, UserOut, Token, UserLogin

router = APIRouter(
    prefix="/accounts",
)


@router.post("/register", response_model=UserOut)
def create_user(
        user: UserCreate,
        session: Session = Depends(get_session),
):
    return User.Objects.create_user(session=session, user=user)


@router.post("/login/", response_model=Token)
def login(
        user: UserLogin,
        session: Session = Depends(get_session),
):
    db_user = auth.authenticate(session=session, email=user.email, password=user.password)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/user/", response_model=UserOut)
def get_user(current_user: User = Depends(auth.get_current_active_user)):
    return current_user
