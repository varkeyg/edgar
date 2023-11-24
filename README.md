# edgar

Edgar Download tools

## Installation
install poetry: https://python-poetry.org/docs/

```bash
git clone git@github.com:varkeyg/edgar.git
cd edgar
poetry install

```


## Running
Change the date in tests/test_edgar.py and run. this will generate  data.csv 
```poetry run pytest -s```

## Usage

- TODO

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`edgar` was created by Geo Varkey. It is licensed under the terms of the MIT license.

## Credits

`edgar` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).


## Data Format
Nodes:
SIC - standard Instrial classifications
CIK - Central Index Key - Holdings
CUSIP - Security Reference

Edges
CIK -[CLASSIFICATION]->SIC
CIK-[REPORTING_PERIOD(Quantity, market value)]->CUSIP