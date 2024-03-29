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

  ``python -m pip install --upgrade pip``

  ``python setup.py install``

  This will install the commands to local system

  **for distrubation**

  ``pip install -U wheel``

  ``python setup.py dists``

  This will create a .whl distrubation under dist/ directory

  ``pip install dist/*.whl``

  This will install the commands to local system

  **for development purpose**

  ``pip install -r requirements.txt``

  ``pip install -e <path-to-mnutree>``

For example say **path-to-mnutree** is user's download folder at ``~/Downloads``.
The following can be executed.

with python
-----------
  ``$ cd  ~/Downloads/mnutree/``

  ``$ python setup.py install``

with pip
---------
  ``$ pip install -e ~/Downloads/mnutree``

for pytest
----------
  ``$ cd ~/Downloads/mnutree``

  **and fire command**

  ``$ python -m pytest -s --cov tests/``

  **or**

  ``$ py.test -s --cov tests/``

  **or**

  ``$ coverage run --source mnutree,mnuapi -m pytest``

  ``$ coverage report``

  **for BDD testing**

  ``$ python -m pytest -s -k "service" ``

  **for HTML report**

  ``$ pytest --html=report.html --self-contained-html``

for documentation
-----------------
  ``$ cd ~/Downloads/mnutree/``

  ``$ make -C docs html``

  the html file will be avilable under ``build/sphinx/html/``

  make command should be avilable in the system

for type checking
-----------------
  ``$ cd ~/Downloads/mnutree/``

  ``$ mypy src/``

  ``$ mypy --ignore-missing-imports tests/``


The ``$ python setup.py install`` will install the commands `mnutree` & `mnuapi`. Please type `mnutree -h` to see the options as:-
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

  The **mnutree** command can also takes the csv file as command line parameter like

  ``$ mnutree -v ~/Downloads/data.csv``

  **or**

  ``$ mnutree -v ~/Downloads/xyz.csv``

  ``$ mnuapi -v`` will start the api server. The swagger-ui is located at http://127.0.0.1:5000/docs
  Please press Ctrl+c to quit the server

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
