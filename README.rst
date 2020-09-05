=======
mnutree
=======

A json menu tree generator from csv file

The file generator comes with a mock data CSV that represents one of the many types of data that we have to deal with at retailshop.
The challenge is to consume and transform the CSV file in to a nested JSON file which will form a tree structure.

Description
===========
The following stack is used for the project
Python 3.8 (>3.8)
PyScaffold 3.2.3

The project can be installed to the python virtual environment or python host with command
  ``python setup.py install``

  **for development purpose**

  ``pip install -e <path-to-mnutree>``

For example say **path-to-mnutree** is user's download folder at ``~/Downloads``.
The following can be executed.

for pytest
----------
  ``$ cd ~/Downloads/mnutree``

  **and fire command**

  ``$ pytest -s --cov tests/``

  **or**

  ``$ py.test -s --cov tests/``

for documentation
-----------------
  ``$ cd ~/Downloads/mnutree/``

  ``$ make -C docs html``

  the html file will be avilable under ``build/sphinx/html/``

  make command should be avilable in the system

with python
-----------
  ``$ cd  ~/Downloads/mnutree/``

  ``$ python setup.py install``

with pip
---------
  ``$ pip install -e ~/Downloads/mnutree``

This will install the command `mnutree`. Please type `mnutree -h` to see the options as:-
-----------------------------------------------------------------------------------------
usage: mnutree [-h] [--version] [-v] [-vv] [FILE]

The utility to convert structured csv to JSON

positional arguments:
  FILE                 input csv file with menu data

optional arguments:
  -h, --help           show this help message and exit
  --version            show program's version number and exit
  -v, --verbose        set loglevel to INFO
  -vv, --very-verbose  set loglevel to DEBUG

example
-------
  ``$ mnutree -v``

The ``pwd`` / current directory should have **data.csv** file. The **mnutree** command takes the csv file as option

  ``$ mnutree -v ~/Downloads/data.csv``

  **or**

  ``$ mnutree -v ~/Downloads/xyz.csv``

Docker Local & Production
=========================
* The development server is started with ``$ docker-compose up``
* The production image is created locally with ``$ docker build . --target production -t mnutree``
* The production image is run as ``$ docker run -p 8080:8080 --env "PORT=8080" -it mnutree``

Note
====
The api uses uvicorn & gunicorn to serve high performance RESTFul requests.
A multi stage docker set up is created for the API.

This project has been set up using PyScaffold 3.2.3. For details and usage
information on PyScaffold see https://pyscaffold.org/.
