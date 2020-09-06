# -*- coding: utf-8 -*-
"""This module contains step definitions for service.feature.
"""

import json
from typing import Dict, Tuple

import pytest
from httpx import AsyncClient, Response
from pytest_bdd import scenarios, given, then, parsers

from mnuapi import app
from mnutree import strfile

HEADER_STR: str = "Base URL,Level 1 - Name,Level 1 - ID,Level 1 - URL,\
    Level 2 - Name,Level 2 - ID,Level 2 URL,Level 3 - Name,Level 3 - ID,Level 3 URL"

# Scenarios
scenarios('../features', example_converters=dict(csv_string=str, json_string=str))

# Given Steps  scope='session'
@pytest.mark.asyncio
@given(parsers.parse('I post "<csv_string>" data to the process API method'),
    target_fixture="api_response")
async def call_api(csv_string: str) -> Tuple:
    """The step to call the file uploading api method
       The step also provides fixtures called "api_response"
       to the other verification steps
    """

    async_client: AsyncClient
    async with AsyncClient(app=app, base_url="http://test") as async_client:
        file_name: str
        with strfile(HEADER_STR+"\n"+csv_string) as file_name:
            with open(file_name, "rb") as file:
                async_response: Response = await async_client.post("/v1/mnutree/process", files={"uploaded_file": file})
    response: Response = async_response

    assert response
    response_data: Dict = response.json()
    assert response_data
    assert response.status_code
    assert response_data["data"]
    return response.status_code, json.dumps(response_data["data"])

# Then Steps
@then(parsers.parse('The valid "<json_string>" as the converted JSON tree'))
def verify_response_contents(api_response: Tuple, json_string: str) -> None:
    """The step to verify that the CSV line is
       converted to the valid & desired JSON tree
    """

    assert  api_response
    assert  api_response[1]
    assert json_string == api_response[1]

@then(parsers.parse('I should get the valid "{code:d}" response'))
def verify_response_code(api_response: Tuple, code: int) -> None:
    """The step to verify the  API
       response code
    """
    assert api_response
    assert api_response[0]
    assert code == api_response[0]

@pytest.mark.asyncio
@given(parsers.parse('I call the GET health end-point'), target_fixture="health_response")
async def call_health_api() -> int:
    """The step to call the health check api method
       The step also provides fixtures called "health_response"
       to the other verification steps
    """
    async with AsyncClient(app=app, base_url="http://test") as async_client:
        response: Response = await async_client.get("/health")

    assert response
    assert response.status_code
    assert response.json()

    return response.status_code

@then(parsers.parse('I should get "{code:d}" response code'))
def verify_health_code(health_response: int, code: int) -> None:
    """The step to verify the  API
       response code
    """
    assert health_response
    assert code == health_response
