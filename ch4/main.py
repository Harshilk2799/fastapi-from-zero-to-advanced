from fastapi import FastAPI

app = FastAPI()

# Single Query Parameter
@app.get("/single_product")
async def single_product_query(category: str):
    return {"status": "OK", "category": category}

# Multiple Query Parameter
@app.get("/multiple_product")
async def multiple_product_query(category: str, limit: int):
    return {"status": "OK", "category": category, "limit": limit}


# Default Query Parameter
@app.get("/default_product")
async def default_product_query(category: str, limit: int = 10):
    return {"status": "OK", "category": category, "limit": limit}

# Optional Query Parameter
@app.get("/optional_product")
async def optional_product_query(limit: int, category: str | None = None):
    return {"status": "OK", "category": category, "limit": limit}

# Path Parameter and Query Parameter
@app.get("/product/{year}")
async def path_query_product(year: int, category: str):
    return {"status": "OK", "year": year, "category": category}