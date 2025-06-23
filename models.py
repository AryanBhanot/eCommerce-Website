from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    balance: float = Field(default=0.0)

    cart_items: List["CartItem"] = Relationship(back_populates="user")
    ratings: List["Rating"] = Relationship(back_populates="user")


class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    price: float = Field(gt=0)
    
    cart_items: List["CartItem"] = Relationship(back_populates="product")
    ratings: List["Rating"] = Relationship(back_populates="product")


class CartItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    product_id: int = Field(foreign_key="product.id")
    quantity: int = Field(default=1)

    user: User = Relationship(back_populates="cart_items")
    product: Product = Relationship(back_populates="cart_items")


class Rating(SQLModel, table=True):
    "Rating model for products."
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    product_id: int = Field(foreign_key="product.id")
    score: int = Field(ge=1, le=5)
    review: Optional[str] = None

    user: User = Relationship(back_populates="ratings")
    product: Product = Relationship(back_populates="ratings")