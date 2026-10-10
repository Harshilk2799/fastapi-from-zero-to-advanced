from fastapi import FastAPI, Depends, Header, HTTPException, APIRouter
from typing import Annotated

app = FastAPI()

# Dependencies in Path Operation Decorations
async def verify_token(x_token: Annotated[str, Header()]):
    if x_token != "my-secret-token":
        raise HTTPException(status_code=400, detail="X-Toen Header invalid!")
    
@app.get("/items", dependencies=[Depends(verify_token)])
async def read_items():
    return {"data": "All items"}


# Dependencies for a group of path operations
router = APIRouter(tags=["User"],prefix="/users",dependencies=[Depends(verify_token)])

app.include_router(router)

@router.get("/")
async def get_all_user():
    return {"data": "All user"}

@router.get("/{user_id}")
async def get_user(user_id: int):
    return {"data": "Single User"}