from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from database import get_session
from models import User
import crud
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/users", tags=["users"])

class UserCreate(BaseModel):
    username: str
    email: str
    balance: float = 0.0

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    balance: Optional[float] = None

@router.post("/", response_model=User)
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    return crud.create_user(session, user.username, user.email, user.balance)

@router.get("/{user_id}", response_model=User)
def get_user(user_id: int, session: Session = Depends(get_session)):
    return crud.get_user_by_id(session, user_id)

@router.put("/{user_id}", response_model=User)
def update_user(
    user_id: int,
    user: UserUpdate,
    session: Session = Depends(get_session)
):
    return crud.update_user(session, user_id, user.dict(exclude_unset=True))

@router.delete("/{user_id}")
def delete_user(user_id: int, session: Session = Depends(get_session)):
    return crud.delete_user(session, user_id)

@router.get("/", response_model=List[User])
def get_all_users(session: Session = Depends(get_session)):
    """Get all users."""
    return session.exec(select(User)).all()
