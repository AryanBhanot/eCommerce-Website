from fastapi import APIRouter, Depends
from sqlmodel import Session
from database import get_session
from models import Rating
import crud
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/ratings", tags=["ratings"])

class RatingCreate(BaseModel):
    user_id: int
    product_id: int
    score: int
    review: Optional[str] = None

@router.post("/", response_model=Rating)
def create_rating(rating: RatingCreate, session: Session = Depends(get_session)):
    return crud.create_rating(
        session,
        rating.user_id,
        rating.product_id,
        rating.score,
        rating.review
    )

@router.get("/product/{product_id}", response_model=list[Rating])
def get_product_ratings(product_id: int, session: Session = Depends(get_session)):
    return crud.get_product_ratings(session, product_id)

@router.get("/user/{user_id}", response_model=list[Rating])
def get_user_ratings(user_id: int, session: Session = Depends(get_session)):
    return crud.get_user_ratings(session, user_id)

@router.delete("/{rating_id}")
def delete_rating(rating_id: int, session: Session = Depends(get_session)):
    return crud.delete_rating(session, rating_id)
