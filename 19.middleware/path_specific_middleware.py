from fastapi import FastAPI, Request

app = FastAPI()

# Creating Middleware 
@app.middleware("http")
async def users_only_middleware(request: Request, call_next):
    if request.url.path.startswith("/users"):
        print("User Middleware: before processing the request!")
        print(f"User Request: {request.method} {request.url}")

        response = await call_next(request)
        print("User Middleware: after proccessing the request, before returning response")
        print(f"User Response status code: {response.status_code}")

        return response 
    else:
        print(f"User Middleware: Skipping middleware for {request.url.path}")
        response = await call_next(request)
        return response 


@app.middleware("http")
async def products_only_middleware(request: Request, call_next):
    if request.url.path.startswith("/products"):
        print("Product Middleware: before processing the request!")
        print(f"Product Request: {request.method} {request.url}")

        response = await call_next(request)
        print("Product Middleware: after proccessing the request, before returning response")
        print(f"Product Response status code: {response.status_code}")

        return response 
    else:
        print(f"Product Middleware: Skipping middleware for {request.url.path}")
        response = await call_next(request)
        return response 


@app.middleware("http")
async def my_middleware(request: Request, call_next):
    print("My Middleware: before processing the request!")
    print(f"My Request: {request.method} {request.url}")

    response = await call_next(request)
    print("My Middleware: after proccessing the request, before returning response")
    print(f"My Response status code: {response.status_code}")

    return response 


@app.get("/users")
async def get_users():
    print("Endpoint: Inside get_users endpoint")
    return {"data": "All users data"}

@app.get("/products")
async def get_products():
    print("Endpoint: Inside get_products endpoint")
    return {"data": "All products data"}