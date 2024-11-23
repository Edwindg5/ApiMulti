from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.shared.config.db import engine, Base
from app.routes import upload

from app.routes import (
    categories_routes,
    item_routes,
    trade_routes,
    shopping_cart_routes,
    transaction_history_routes,
    loan_items_routes,
    rating_history_routes,
    notification_routes,
    users_routes,
    
)

# Crear tablas en la base de datos si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambia esto a los dominios específicos de tu frontend en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir todas las rutas de los módulos de la aplicación
app.include_router(upload.router, prefix="/api", tags=["Upload"])
app.include_router(users_routes.router, prefix="/users", tags=["Users"])
app.include_router(categories_routes.router, tags=["Categories"])
app.include_router(item_routes.router, tags=["Items"])
app.include_router(trade_routes.router, prefix="/trades", tags=["Trades"])
app.include_router(shopping_cart_routes.router, prefix="/shopping-cart", tags=["Shopping Cart"])
app.include_router(transaction_history_routes.router, prefix="/transaction-history", tags=["Transaction History"])
app.include_router(loan_items_routes.router, prefix="/loan-items", tags=["Loan Items"])
app.include_router(rating_history_routes.router, prefix="/rating-history", tags=["Rating History"])
app.include_router(notification_routes.router, prefix="/notifications", tags=["Notifications"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI project!"}
