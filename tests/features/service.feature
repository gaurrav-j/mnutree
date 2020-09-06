# -*- coding: utf-8 -*-

@service @mnutree
Feature: MENU TREE CSV TO JSON CONVERSION API
    As an application developer,
    I want to upload a menu tree CSV file via a REST API,
    So that a JSON conversion of CSV file is received.

    Scenario Outline: Mnutree Process API Call
        Given I post "<csv_string>" data to the process API method
        Then I should get the valid "200" response
        And The valid "<json_string>" as the converted JSON tree

        Examples: Animals
        | csv_string | json_string |
        | https://link.com,THE BEST,178974,https://link.com/178974   | [{"label": "THE BEST", "id": "178974", "link": "https://link.com/178974"}] |
        | https://link.com,THE BEST,178974,https://link.com/178974,FRESH,178969,https://link.com/178974/178969 | [{"label": "THE BEST", "id": "178974", "link": "https://link.com/178974", "children": [{"label": "FRESH", "id": "178969", "link": "https://link.com/178974/178969"}]}] |
        | https://link.com,THE BEST,178974,https://link.com/178974,SECOND BEST,178975,https://link.com/178975  | [{"label": "THE BEST", "id": "178974", "link": "https://link.com/178974"}, {"label": "SECOND BEST", "id": "178975", "link": "https://link.com/178975"}] |
        | https://link.com,THE BEST,178974,https://link.com/178974,FRESH,178969,https://link.com/178974/178969,FRESH ONE,178970,https://link.com/178974/178969/178970,FRESH TWO,178971,https://link.com/178974/178969/178970/178971 | [{"label": "THE BEST", "id": "178974", "link": "https://link.com/178974", "children": [{"label": "FRESH", "id": "178969", "link": "https://link.com/178974/178969", "children": [{"label": "FRESH ONE", "id": "178970", "link": "https://link.com/178974/178969/178970", "children": [{"label": "FRESH TWO", "id": "178971", "link": "https://link.com/178974/178969/178970/178971"}]}]}]}] |
        | https://link.com,THE BEST,178974,https://link.com/178974,SECOND BEST,178975,https://link.com/178975,FRESH,178969,https://link.com/178974/178969,FRESH ONE,178970,https://link.com/178974/178969/178970,FRESH TWO,178971,https://link.com/178974/178969/178970/178971 | [{"label": "THE BEST", "id": "178974", "link": "https://link.com/178974", "children": [{"label": "FRESH", "id": "178969", "link": "https://link.com/178974/178969", "children": [{"label": "FRESH ONE", "id": "178970", "link": "https://link.com/178974/178969/178970", "children": [{"label": "FRESH TWO", "id": "178971", "link": "https://link.com/178974/178969/178970/178971"}]}]}]}, {"label": "SECOND BEST", "id": "178975", "link": "https://link.com/178975"}] |


    Scenario Outline: Mnutree Health Check Call
        Given I call the GET health end-point
        Then I should get "200" response code