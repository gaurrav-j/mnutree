# -*- coding: utf-8 -*-
"""This is a main file that can serve as a starting point for a Python console script.
   console_scripts =
        mnutree = mnutree.main:run

   Then run `python setup.py install` which will install the
   command `mnutree` inside your current environment.
   Besides console scripts, the header (i.e. until logger...) of this module can
   also be used as template for Python modules.
"""
import sys
import json
from pathlib import Path
from types import SimpleNamespace
from typing import List, TextIO, Dict, Union, Any

from mnutree import info
from mnutree import parse_args
from mnutree import setup_logging
from mnutree.processor import process

__author__ = "Gaurav J"
__copyright__ = "Mastek India Pvt. Ltd"
__license__ = "MIT"

def main(args: Any) -> None:
    """Main entry point allowing external calls

       Parameters
       ----------
       args: ([str])
        command line parameter list
    """
    if not isinstance(args, SimpleNamespace):
        args = parse_args(args)

    setup_logging(args.loglevel)
    info("Starting JSON conversion...")

    menus: List[Dict[str, Union[str, Any]]]
    file_path: Path
    json_file: TextIO

    file_path , menus  = process(args)

    menus_str: str = json.dumps(menus)

    with file_path.open("w") as json_file:
        json_file.writelines(menus_str)

    info("Conversion to JSON ends here")

def run() -> None:
    """Entry point for console_scripts
    """

    main(sys.argv[1:])

if __name__ == "__main__":
    run()
