from fastapi import FastAPI

class CustomLoggingMiddleware:
    def __init__(self, app, prefix="LOG"):
        self.app = app 
        self.prefix = prefix

    async def __call__(self, scope, receive, send):
        print(f"{self.prefix}: Before processing request (scope: {scope})")
        await self.app(scope, receive, send)
        print(f"{self.prefix}: After processing request")

app = FastAPI()
app.add_middleware(CustomLoggingMiddleware, prefix="CUSTOM_LOG")


@app.get("/users")
async def get_users():
    print("Endpoint: Inside get_users endpoint")
    return {"data": "All users data"}

@app.get("/products")
async def get_products():
    print("Endpoint: Inside get_products endpoint")
    return {"data": "All products data"}