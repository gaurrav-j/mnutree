# -*- coding: utf-8 -*-
"""The test script for the main module
"""
from pathlib import Path
from mnutree.main import main

def test_main(cmd_arg):
    """The method to test main
    """
    main(cmd_arg)

    if cmd_arg.csv_file.find("/") > -1:
        file_path = Path(cmd_arg.csv_file)
    else:
        file_path = Path("./"+cmd_arg.csv_file)

    file_path = file_path.with_suffix('.json')

    assert file_path.exists()
    assert file_path.is_file()
