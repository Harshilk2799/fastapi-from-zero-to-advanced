from fastapi import FastAPI, Depends
from typing import Annotated

app = FastAPI()

# sync dependency 
def sync_dep():
    return {"message": "I am sync"}

@app.get("/sync")
def test(sync_result: Annotated[dict, Depends(sync_dep)]):
    return {"sync": sync_result}


# async dependency
async def async_dep():
    return {"message": "I am async"}

@app.get("/async")
async def test(
    sync_result: Annotated[dict, Depends(sync_dep)],
    async_result: Annotated[dict, Depends(async_dep)]):
    return {"sync": sync_result, "async": async_result}