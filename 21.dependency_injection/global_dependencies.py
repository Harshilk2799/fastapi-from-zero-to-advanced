from fastapi import FastAPI, Depends, Header, HTTPException, APIRouter
from typing import Annotated

# Dependencies in Path Operation Decorations
async def verify_token(x_token: Annotated[str, Header()]):
    if x_token != "my-secret-token":
        raise HTTPException(status_code=400, detail="X-Toen Header invalid!")

app = FastAPI(dependencies=[Depends(verify_token)])
    
@app.get("/items", dependencies=[Depends(verify_token)])
async def read_items():
    return {"data": "All items"}

