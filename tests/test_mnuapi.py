# -*- coding: utf-8 -*-
"""The test script for testing the api
"""

import pytest
from httpx import AsyncClient

from mnuapi import app

@pytest.mark.asyncio
async def test_health():
    """The method to test the health of
       file processing api
    """
    async with AsyncClient(app=app, base_url="http://test") as async_client:
        response = await async_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

@pytest.mark.asyncio
async def test_accept_file():
    """The method to test the file uploading
       api method
    """
    async with AsyncClient(app=app, base_url="http://test") as async_client:
        with open("tests/data.csv", "rb") as file:
            response = await async_client.post("/v1/mnutree/process", files=file)
    print(response)
    assert response.json() is not None
