[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/IwJY4g24)

# Bank-app

## Author:

name: Daria

surname: Zverieva

group: 2

## How to start the app

### Installation

```bash
pip install -r requirements.txt
```

### Start MongoDB

```bash
docker compose -f mongo.yml up -d
```

### Run Flask API

For Linux/Mac:

```bash
export FLASK_APP=app.api:app
export FLASK_ENV=development
export PYTHONPATH=$PWD
flask run
```

For Windows:

```bash
set FLASK_APP=app.api:app
set FLASK_ENV=development
set PYTHONPATH=%cd%
flask run
```

The API will be available at `http://127.0.0.1:5000`

## How to execute tests

### Unit tests with coverage

```bash
python -m coverage run --source=src -m pytest tests/unit
python -m coverage report -m
```

Generate HTML coverage report:

```bash
python -m coverage html
```

### API tests

```bash
python -m pytest tests/api
```

### Performance tests

```bash
python -m pytest tests/perf
```

### BDD tests (Behave)

```bash
pip install behave
behave
```
