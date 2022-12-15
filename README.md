This is a project that uses pipenv to manage dependencies.

## Installation

To install dependencies using pipenv, first you must install pipenv on your MacOS system.

1. Install pipenv by running the following command:

```
pip install pipenv
```

2. Once pipenv is installed, navigate to the directory of your project and run the following command to create a virtual environment and install all dependencies listed in your \`Pipfile\`:

```
pipenv install
```

3. To activate the virtual environment, run the following command:

```
pipenv shell
```

5. To exit the virtual environment, run the following command:

```
exit
```

## Usage

To use this script, run the following command:

```
python json_to_avsc.py <json_file> [-o <output_file>]
```