from sqlmodel import Session, select
from models import User, Product, CartItem, Rating
from typing import List, Optional, Dict
from fastapi import HTTPException
import re

def create_user(session: Session, username: str, email: str, balance: float = 0.0) -> User:
    "Creates a new user with given username, email and optional balance."
    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if not re.match(email_pattern, email):
        raise HTTPException(status_code=400, detail="Invalid email format")
    if not username or not email:
        raise HTTPException(status_code=400, detail="Username and email are required")
    if balance < 0:
        raise HTTPException(status_code=400, detail="Balance cannot be negative")
    
    existing_user = session.exec(select(User).where(User.email == email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
        
    user = User(username=username, email=email, balance=balance)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def get_user_by_id(session: Session, user_id: int) -> User:
    """Retrieves a user by ID."""
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def update_user(session: Session, user_id: int, update_data: Dict) -> User:
    """Updates user information."""
    user = get_user_by_id(session, user_id)
    for key, value in update_data.items():
        if value is not None:
            setattr(user, key, value)
    session.commit()
    session.refresh(user)
    return user

def delete_user(session: Session, user_id: int):
    """Deletes a user."""
    user = get_user_by_id(session, user_id)
    session.delete(user)
    session.commit()
    return {"message": "User deleted successfully"}

def create_product(session: Session, name: str, description: str, price: float) -> Product:
    """Creates a new product."""
    if not name or not description:
        raise HTTPException(status_code=400, detail="Name and description are required")
    if price <= 0:
        raise HTTPException(status_code=400, detail="Price must be greater than 0")
        
    # Check if product with same name exists
    existing_product = session.exec(select(Product).where(Product.name == name)).first()
    if existing_product:
        raise HTTPException(status_code=400, detail="Product with this name already exists")
        
    product = Product(name=name, description=description, price=price)
    session.add(product)
    session.commit()
    session.refresh(product)
    return product

def get_products(session: Session) -> List[Product]:
    """Returns list of all products."""
    return list(session.exec(select(Product)).all())

def get_product_by_id(session: Session, product_id: int) -> Dict:
    """Gets a product with its ratings."""
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    ratings = session.exec(select(Rating).where(Rating.product_id == product_id)).all()
    avg_rating = 0.0
    if ratings:
        avg_rating = sum(r.score for r in ratings) / len(ratings)
    
    return {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "average_rating": round(avg_rating, 2),
        "total_ratings": len(ratings)
    }

def update_product(session: Session, product_id: int, update_data: Dict) -> Product:
    """Updates product information."""
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    for key, value in update_data.items():
        if value is not None:
            if key == "price" and value <= 0:
                raise HTTPException(status_code=400, detail="Price must be greater than 0")
            setattr(product, key, value)
    
    session.commit()
    session.refresh(product)
    return product

def delete_product(session: Session, product_id: int):
    """Deletes a product."""
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    session.delete(product)
    session.commit()
    return {"message": "Product deleted successfully"}

def get_user_cart(session: Session, user_id: int) -> List[CartItem]:
    """Gets all cart items for a user."""
    user = get_user_by_id(session, user_id)
    return session.exec(select(CartItem).where(CartItem.user_id == user_id)).all()

def add_to_cart(session: Session, user_id: int, product_id: int, quantity: int = 1) -> CartItem:
    """Adds or updates an item in the cart."""
    if quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than 0")
    
    user = get_user_by_id(session, user_id)
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    cart_item = session.exec(
        select(CartItem).where(
            CartItem.user_id == user_id,
            CartItem.product_id == product_id
        )
    ).first()

    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(user_id=user_id, product_id=product_id, quantity=quantity)
        session.add(cart_item)

    session.commit()
    session.refresh(cart_item)
    return cart_item

def update_cart_item(session: Session, cart_item_id: int, quantity: int) -> CartItem:
    """Updates the quantity of a cart item."""
    if quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than 0")
    
    cart_item = session.get(CartItem, cart_item_id)
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    
    cart_item.quantity = quantity
    session.commit()
    session.refresh(cart_item)
    return cart_item

def remove_from_cart(session: Session, cart_item_id: int):
    """Removes an item from the cart."""
    cart_item = session.get(CartItem, cart_item_id)
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    session.delete(cart_item)
    session.commit()
    return {"message": "Item removed from cart"}

def create_rating(session: Session, user_id: int, product_id: int, score: int, review: Optional[str] = None) -> Rating:
    """Creates a product rating."""
    if score < 1 or score > 5:
        raise HTTPException(status_code=400, detail="Score must be between 1 and 5")
    
    user = get_user_by_id(session, user_id)
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    existing_rating = session.exec(
        select(Rating).where(
            Rating.user_id == user_id,
            Rating.product_id == product_id
        )
    ).first()

    if existing_rating:
        raise HTTPException(status_code=400, detail="User has already rated this product")

    rating = Rating(
        user_id=user_id,
        product_id=product_id,
        score=score,
        review=review
    )
    session.add(rating)
    session.commit()
    session.refresh(rating)
    return rating

def get_product_ratings(session: Session, product_id: int) -> List[Rating]:
    """Gets all ratings for a product."""
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return session.exec(select(Rating).where(Rating.product_id == product_id)).all()

def get_user_ratings(session: Session, user_id: int) -> List[Rating]:
    """Gets all ratings by a user."""
    user = get_user_by_id(session, user_id)
    return session.exec(select(Rating).where(Rating.user_id == user_id)).all()

def delete_rating(session: Session, rating_id: int):
    """Deletes a rating."""
    rating = session.get(Rating, rating_id)
    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found")
    session.delete(rating)
    session.commit()
    return {"message": "Rating deleted successfully"}

def clear_cart(session: Session, user_id: int):
    cart_items = session.exec(
        select(CartItem).where(CartItem.user_id == user_id)
    ).all()
    
    for item in cart_items:
        session.delete(item)
    
    session.commit()
    return {"message": "Cart cleared successfully"}