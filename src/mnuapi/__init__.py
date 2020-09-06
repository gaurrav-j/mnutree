# -*- coding: utf-8 -*-
"""The api for the menu tree menu generator.
   The file can be uploaded from the swagger-ui
"""

import os
from typing import List, TextIO, Dict, Union, Any

from fastapi.applications import FastAPI
import uvicorn # type: ignore

from mnuapi.req_processor import  router

app: FastAPI = FastAPI(title=__name__, description="A json menu tree generator from csv file")
app.include_router(router, prefix='/v1/mnutree')

@app.get("/health", tags=["health-check"], responses={
    200: {"description": "api is ok"},
    400: {"description": "bad request"},
    500: {"description": "internal server error"}
})
def health() -> Dict[str, str]:
    """The health check for menu api
    """
    return {"status": "ok"}

def run() -> None:
    """Entry point for api server
    """
    uvicorn.run("mnuapi:app", host="127.0.0.1", port=5000, log_level="info")
