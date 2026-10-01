from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import Annotated

app = FastAPI()

# application/x-www-form-urlencoded
# multipart/form-data

# Simple HTML form for testing
@app.get("/", response_class=HTMLResponse)
async def get_form():
    return """
    <html>
        <body>
            <h2>Login Form</h2>
            <form action="/login/" method="POST">
                <label for="username">Username</label><br>
                <input type="text" id="username" name="username"><br>
                <label for="password">Password</label><br>
                <input type="text" id="password" name="password"><br>
                <input type="submit" value="Submit">
            </form>
        </body>
    </html>
    """

# @app.post("/login/")
# async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
#     return {"username": username, "password_length": len(password)}

# @app.post("/login/")
# async def login(
#     username: Annotated[str, Form(min_length=3)], 
#     password: Annotated[str, Form(min_length=3, max_length=20)]
#     ):
#     return {"username": username, "password_length": len(password)}


# Form Data with Pydantic Model
# class FormData(BaseModel):
#     username: str 
#     password: str 

# @app.post("/login/")
# async def login(data: Annotated[FormData, Form()]):
#     return data


# Pydantic models for forms with Validation
class FormData(BaseModel):
    username: str = Field(min_length=3)
    password: str = Field(min_length=3, max_length=20)

@app.post("/login/")
async def login(data: Annotated[FormData, Form()]):
    return data
