# Python testing tutorial

## Set up

1. Create virtual environment: `python -m venv .venv --prompt pytest-tutorial`
1. Activate the virtual environment: `source .venv/bin/activate`
1. Install the tutorial module: `pip install -e .`
1. Install other dependencies: `pip install -r requirements.txt`
1. Run the tests `pytest -v -s`

Take a look through `tests/test_mocks.py` for various ways on using python mocks and patching to test things.
