from fastapi import APIRouter, Depends
from sqlmodel import Session
from database import get_session
from models import CartItem
import crud
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/cart", tags=["cart"])

class CartAdd(BaseModel):
    user_id: int
    product_id: int
    quantity: int = 1

class CartUpdate(BaseModel):
    quantity: int

@router.post("/", response_model=CartItem)
def add_to_cart(cart_item: CartAdd, session: Session = Depends(get_session)):
    return crud.add_to_cart(
        session, 
        cart_item.user_id, 
        cart_item.product_id, 
        cart_item.quantity
    )

@router.get("/{user_id}", response_model=list[CartItem])
def get_user_cart(user_id: int, session: Session = Depends(get_session)):
    return crud.get_user_cart(session, user_id)

@router.put("/{cart_item_id}", response_model=CartItem)
def update_cart_item(
    cart_item_id: int,
    cart_update: CartUpdate,
    session: Session = Depends(get_session)
):
    return crud.update_cart_item(session, cart_item_id, cart_update.quantity)

@router.delete("/{cart_item_id}")
def remove_from_cart(cart_item_id: int, session: Session = Depends(get_session)):
    return crud.remove_from_cart(session, cart_item_id)
