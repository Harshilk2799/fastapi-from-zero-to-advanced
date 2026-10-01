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
            <h2>Multiple Files Upload(bytes)</h2>
            <form action="/uploadfiles/" enctype="multipart/form-data" method="POST">
                <input type="file" multiple name="files"><br>
                <input type="submit" value="Submit">
            </form>
        </body>
    </html>
    """


@app.post("/uploadfiles/")
async def create_upload_file(files: Annotated[list[UploadFile], File()]):
    save_files = []
    os.makedirs("uploads", exist_ok=True)

    for file in files:
        save_path = f"uploads/{file.filename}"
        with open(save_path, "wb") as buffer:
           shutil.copyfileobj(file.file, buffer)
        save_files.append({"filename": file.filename})
       
    return save_files