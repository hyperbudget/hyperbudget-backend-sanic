# hyperbudget-backend-sanic

Sanic-based backend for https://api.hyperbudget.net/

## Configure

```
cp .env.example .env
```

Add api keys in `.env`

## Install & Run

### Without docker

* Install pipenv and python 3.7, then:

```
pinenv install
pienv run python app.py
```

### With docker

```
docker build -t hbbackend .
docker run hbbackend
```
