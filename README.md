# eCommerce API

A RESTful API for an eCommerce platform built with FastAPI and SQLModel. This project supports user management, product catalog, shopping cart, and product ratings.

## Features
- User registration, update, and deletion
- Product creation, listing, update, and deletion
- Shopping cart management (add, update, remove items)
- Product rating and review system
- SQLite database with SQLModel ORM
- Modular service structure
- Interactive API docs via Swagger UI

## Project Structure
```
├── crud.py                # Database CRUD operations
├── database.py            # Database connection and session management
├── ecommerce.db           # SQLite database file
├── main.py                # FastAPI app entry point
├── models.py              # SQLModel ORM models
├── requirements.txt       # Python dependencies
├── services/              # API routers for each domain
│   ├── cart_service.py
│   ├── product_service.py
│   ├── rating_service.py
│   └── user_service.py
└── README.md              # Project documentation
```

## Getting Started

### Prerequisites
- Python 3.8+

### Installation
1. Clone the repository and navigate to the project directory.
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Start the development server:
   ```sh
   uvicorn main:app --reload
   ```
4. Access the API docs at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## API Endpoints

### Users
- `POST /users/` - Create a new user
- `GET /users/` - Get all users
- `GET /users/{user_id}` - Get a user by ID
- `PUT /users/{user_id}` - Update a user
- `DELETE /users/{user_id}` - Delete a user

### Products
- `POST /products/` - Create a new product
- `GET /products/` - List all products
- `GET /products/{product_id}` - Get product details (with ratings)
- `PUT /products/{product_id}` - Update a product

### Cart
- `POST /cart/` - Add item to cart
- `GET /cart/{user_id}` - Get user's cart
- `PUT /cart/{cart_item_id}` - Update cart item quantity
- `DELETE /cart/{cart_item_id}` - Remove item from cart

### Ratings
- `POST /ratings/` - Add a rating to a product
- `GET /ratings/product/{product_id}` - Get all ratings for a product
- `GET /ratings/user/{user_id}` - Get all ratings by a user
- `DELETE /ratings/{rating_id}` - Delete a rating

## Database
- Uses SQLite by default (`ecommerce.db`).
- Tables are auto-created on server startup.