[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Project generated with PyScaffold](https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold)](https://pyscaffold.org/)

# activity-logger

> Flask Application to log activities

A longer description of your project goes here...

## Getting Started

### Install Python

Please follow
[this instructions](https://pages.github.hexagon.com/geo-surv/python-package-documentation/python-environment/development-workflow/)
to install python. This package requires
[python3.8](https://www.python.org/downloads/release/python-3810/).

### Python Environment

Create or synchronize your "pipenv" with

```bash
pipenv sync
```

This will automatically update your project environment with the necessary python packages.
If you are interested in further details, please read
[this section](https://pages.github.hexagon.com/geo-surv/python-package-documentation/recommended-packages/virtual-environment/#pipenv).


### Migrate (to create database.sqlite)

```console
set FLASK_APP=app.py
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
```


### Workflows

This project uses
[`tox`](https://pages.github.hexagon.com/geo-surv/python-package-documentation/python-environment/tox-workflow/)
to automate different workflows for you.

#### Stylecheck

The *stylecheck* can be executed with:

```bash
tox -e stylecheck
```

#### Run Static Code Analysis

The *linter* can be run with:

```bash
tox -e lint
```

#### Run Tests

The *tests* can be run with:

```bash
tox -e test
```

#### Project Documentation

The project documentation can be built with

```bash
tox -e docs
```

The built documentation will be located at *docs/_build/html/*.
Github will automatically host the documentation for you [here](add link).

## Python Documentation

Please check out our internal [python documentation](https://pages.github.hexagon.com/geo-surv/python-package-documentation/) for more information.

## Note

This project has been set up using PyScaffold 4.5. For details and usage
information on PyScaffold see https://pyscaffold.org/.
