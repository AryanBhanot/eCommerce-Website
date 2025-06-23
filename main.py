from fastapi import FastAPI
import uvicorn
from database import create_db_and_tables
from services.user_service import router as user_router
from services.product_service import router as product_router
from services.cart_service import router as cart_router
from services.rating_service import router as rating_router

app = FastAPI(
    title="eCommerce API",
    version="1.0.0",
    description="A RESTful API for an eCommerce platform with user, product, cart, and rating management"
)

# Include all service routers
app.include_router(user_router)
app.include_router(product_router)
app.include_router(cart_router)
app.include_router(rating_router)

# Startup event
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

