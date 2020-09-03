# -*- coding: utf-8 -*-
"""The api for the menu tree menu generator.
   The file can be uploaded from the swagger-ui
"""

import uvicorn
from fastapi import FastAPI, File, UploadFile

app = FastAPI(title="MenuTree", description="A json menu tree generator from csv file")

@app.post("/files/")
async def create_file(file: bytes = File(...)):
    """The upload file with bytes
    """
    return {"file_size": len(file)}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    """The upload file with file
    """
    return {"filename": file.filename}


def run():
    """Entry point for api server
    """
    uvicorn.run("mnuapi:app", host="127.0.0.1", port=8000, log_level="info")
