# -*- coding: utf-8 -*-
"""The test module
"""
import os
import sys
import tempfile
from contextlib import contextmanager
from typing import Generator

sys.path.append('..')

@contextmanager
def strfile(data: str) -> Generator:
    """The temp file context manager
    """
    temp = tempfile.NamedTemporaryFile(delete=False)
    config_path = f'{temp.name}.csv'
    with open(config_path, 'w') as file:
        file.write(data)
    try:
        yield f'{temp.name}.csv'
    finally:
        temp.close()
        os.unlink(temp.name)
