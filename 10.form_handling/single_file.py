from fastapi import FastAPI, Form, File, UploadFile
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import Annotated
import os
import uuid
import shutil

app = FastAPI()

# Simple HTML form for testing
@app.get("/", response_class=HTMLResponse)
async def main():
    return """
    <html>
        <body>
            <h2>Single File Upload(bytes)</h2>
            <form action="/files/" enctype="multipart/form-data" method="POST">
                <input type="file" name="file"><br>
                <input type="submit" value="Submit">
            </form>
            <h2>Single File Upload(UploadFile)</h2>
            <form action="/uploadfiles/" enctype="multipart/form-data" method="POST">
                <input type="file" name="file"><br>
                <input type="submit" value="Submit">
            </form>
        </body>
    </html>
    """

# @app.post("/files/")
# async def create_file(file: Annotated[bytes | None, File()] = None):
#     if not file:
#         return {"message": "No file sent!"}
#     return {"file_size": len(file)}


# @app.post("/files/")
# async def create_file(file: Annotated[bytes | None, File()] = None):
#     if not file:
#         return {"message": "No file sent!"}
#     filename = f"{uuid.uuid4()}.bin"
#     save_path = f"uploads/{filename}"

#     os.makedirs("uploads", exist_ok=True)

#     with open(save_path, "wb") as buffer:
#         buffer.write(file)
        
#     return {"file_size": len(file)}



@app.post("/files/")
async def create_file(file: Annotated[bytes | None, File()] = None):
    if not file:
        return {"message": "No file sent!"}
    filename = f"{uuid.uuid4()}.bin"
    save_path = f"uploads/{filename}"

    os.makedirs("uploads", exist_ok=True)

    with open(save_path, "wb") as buffer:
        buffer.write(file)
        
    return {"file_size": len(file)}


@app.post("/uploadfiles/")
async def create_upload_file(file: Annotated[UploadFile | None, File()] = None):
    if not file:
        return {"message": "No upload file sent!"}
    
    save_path = f"uploads/{file.filename}"
    os.makedirs("uploads", exist_ok=True)

    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename, "content_type": file.content_type}