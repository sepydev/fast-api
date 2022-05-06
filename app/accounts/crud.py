from sqlmodel import Session, select
from accounts.models import User, UserCreate, UserOut
from fastapi import HTTPException, status


def create_user(session: Session, user: UserCreate):
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
    db_user = User(email=user.email, hashed_password=user.password)
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
