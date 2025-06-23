from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import List, Optional
from database import get_session
from models import Product
import crud
from pydantic import BaseModel

router = APIRouter(prefix="/products", tags=["products"])

class ProductCreate(BaseModel):
    name: str
    description: Optional[str]
    price: float

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None

class ProductWithRating(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    average_rating: float
    total_ratings: int

@router.post("/", response_model=Product)
def create_product(
    product: ProductCreate,
    session: Session = Depends(get_session)
):
    return crud.create_product(session, product.name, product.description or "", product.price)

@router.get("/", response_model=List[Product])
def list_products(session: Session = Depends(get_session)):
    return crud.get_products(session)

@router.get("/{product_id}", response_model=ProductWithRating)
def get_product(product_id: int, session: Session = Depends(get_session)):
    return crud.get_product_by_id(session, product_id)

@router.put("/{product_id}", response_model=Product)
def update_product(
    product_id: int,
    product: ProductUpdate,
    session: Session = Depends(get_session)
):
    return crud.update_product(session, product_id, product.dict(exclude_unset=True))
