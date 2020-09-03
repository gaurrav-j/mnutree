# -*- coding: utf-8 -*-
"""The file used by pytest to auto-discover
   the fixtures and the  data shared amongst various tests.
   This file is included for demo purpose and it is not having a
   very strong use case in this module.
"""

from types import SimpleNamespace
import pytest

@pytest.fixture(scope="module")
def menu_item():
    """The method to show fixture returning
       just the dictionary
    """
    return {
        'label': 'CHEESE',
        'id': '178975',
        'link': 'https://groceries.morrisons.com/browse/178974/178969/178975'
    }


@pytest.fixture(scope="module")
def cmd_arg():
    """The method to return the command line
       arguments for testing purpose
    """
    cmd_input_path = "tests/data.csv"
    args = {"csv_file": cmd_input_path, "loglevel":"20"}

    return SimpleNamespace(**args)
