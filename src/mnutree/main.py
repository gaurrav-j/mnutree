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

from types import SimpleNamespace
from mnutree import info
from mnutree import parse_args
from mnutree import setup_logging
from mnutree.processor import process

__author__ = "Gaurav J"
__copyright__ = "Mastek India Pvt. Ltd"
__license__ = "MIT"

def main(args):
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

    file_path, menus = process(args)
    menus = json.dumps(menus)
    with open(file_path, "w") as json_file:
        json_file.writelines(menus)

    info("Conversion to JSON ends here")

def run():
    """Entry point for console_scripts
    """

    main(sys.argv[1:])

if __name__ == "__main__":
    run()
