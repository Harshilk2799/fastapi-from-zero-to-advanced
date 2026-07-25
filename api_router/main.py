from fastapi import FastAPI
from app.user.routers import router as user_routers
from app.product.routers import router as product_routers

app = FastAPI()

# To defined prefix value make sure every route to remove "/users"

# app.include_router(user_routers, tags=["Users"], prefix="/users")
# app.include_router(product_routers, tags=["Products"], prefix="/products")

app.include_router(user_routers, tags=["Users"])
app.include_router(product_routers, tags=["Products"])

# app.include_router(user_routers)
# app.include_router(product_routers)