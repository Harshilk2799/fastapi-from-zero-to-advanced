from fastapi import FastAPI, Request

app = FastAPI()

# Creating Middleware 
@app.middleware("http")
async def my_first_middleware(request: Request, call_next):
    print("Middleware: before processing the request!")
    print(f"Request: {request.method} {request.url}")

    response = await call_next(request)
    print("Middleware: after proccessing the request, before returning response")
    print(f"Response status code: {response.status_code}")

    return response 

@app.get("/users")
async def get_users():
    print("Endpoint: Inside get_users endpoint")
    return {"data": "All users data"}

@app.get("/products")
async def get_products():
    print("Endpoint: Inside get_products endpoint")
    return {"data": "All products data"}