# -*- coding: utf-8 -*-
"""The test script for testing the api
"""

import pytest
from httpx import AsyncClient

from mnuapi import app
from mnuapi import health

@pytest.mark.asyncio
async def test_health():
    """The method to test the health of
       file processing api
    """
    response = health()
    assert response
    assert {'status': 'ok'} == response

@pytest.mark.asyncio
async def test_accept_file():
    """The method to test the file uploading
       api method
    """
    async with AsyncClient(app=app, base_url="http://test") as async_client:
        with open("tests/data.csv", "rb") as file:
            response = await async_client.post("/v1/mnutree/process", files={"uploaded_file": file})
    respose_data = response.json()

    assert respose_data is not None
    assert respose_data

    assert "message" in respose_data
    assert respose_data["message"] == "The file data.csv of type text/csv processed successfully"
