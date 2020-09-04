# -*- coding: utf-8 -*-
"""The router for menu tree request processing
"""
from io import BytesIO
from typing import List, Dict, Any

from fastapi import APIRouter
from fastapi import File, UploadFile
from fastapi import status, Response, HTTPException

from mnutree import info
from mnutree.processor import normallize, create_menu

router = APIRouter()

@router.post("/process", tags=["process-csv"], responses={
    200: {"description": "file is processed"},
    400: {"description": "bad request"},
    500: {"description": "internal server error"}
})
async def accept_file(response: Response, uploaded_file: UploadFile = File(...)):
    """The method to take file multi-part upload.
       The file is uploaded to the memory
    """
    menu_list: List = []

    try:
        if uploaded_file.content_type != "text/csv":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                detail="Please provide csv file")

        contents = await uploaded_file.read()

        if len(contents) == 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                detail="The uploaded csv file is empty")

        file = BytesIO(contents)

        object_cache: Dict[str, Any] = {}
        line_count: int = 0
        for line in file:
            line = line.rstrip()
            if line_count == 0:
                line_count += 1
                info("process:header: {} ", line, debug=True)
            else:
                line_count += 1
                line_str: str = normallize(line.decode('utf-8'))
                list_of_items_in_line: List = [word for word in line_str.split(',')
                    if word and word != "\n"]
                len_list_of_items_in_line: int = len(list_of_items_in_line)
                info("process: {} . len --> {}, list_of_items_in_line --> {}",
                    line_count, len_list_of_items_in_line, list_of_items_in_line, debug=True)
                if len_list_of_items_in_line != 0:
                    create_menu(list_of_items_in_line, menu_list, object_cache)

    except IOError as error:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "message": f'an error occured {error}'
        }

    return {
        "message":
            f'The file {uploaded_file.filename} of '
            f'type {uploaded_file.content_type} processed successfully',
        "data": menu_list
    }
