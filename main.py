from fastapi import FastAPI
from app.shared.config.db import engine, Base
from app.routes import (
    user_routes,
    category_routes,
    item_routes,
    trade_routes,
    shopping_cart_routes,
    transaction_history_routes,
    loan_items_routes,
    rating_history_routes,
    notification_routes,
)

# Crear tablas en la base de datos si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Incluir todas las rutas de los módulos de la aplicación
app.include_router(user_routes.router, prefix="/users", tags=["Users"])
app.include_router(category_routes.router, prefix="/categories", tags=["Categories"])
app.include_router(item_routes.router, prefix="/items", tags=["Items"])
app.include_router(trade_routes.router, prefix="/trades", tags=["Trades"])
app.include_router(shopping_cart_routes.router, prefix="/shopping-cart", tags=["Shopping Cart"])
app.include_router(transaction_history_routes.router, prefix="/transaction-history", tags=["Transaction History"])
app.include_router(loan_items_routes.router, prefix="/loan-items", tags=["Loan Items"])
app.include_router(rating_history_routes.router, prefix="/rating-history", tags=["Rating History"])
app.include_router(notification_routes.router, prefix="/notifications", tags=["Notifications"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI project!"}
