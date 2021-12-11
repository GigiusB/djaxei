# A django admin extension for importing exporting records from/to xls/ods

A Python library project using:
* pytest
* flake8
* tox
* bumpversion
* isort

* Free software: MIT license
* Documentation: __TBD__


# Features

- Requires Python >=3.6.1
- Currently work only with xlsxwriter

- Could help if use [direnv](https://direnv.net/) in dev environment

* TODO

# Dev setup

1. install direnv
2. install pyenv
3. clone project: `git clone https://github.com/GigiusB/djaxei.git`
4. `cd djaxei`
5. ```pyenv install `cat .python-version` ```
6. `pip install -U poetry` # this should install poetry in your pyenv python
7. `cp .env.example .env`
8. `cp .envrc.example .envrc`
9. `direnv allow`
10. ```poetry env use `pyenv which python` ```
11. `cd .. ; cd -`  # see if it loads the env
12. poetry install
13. pytest

Credits
-------

