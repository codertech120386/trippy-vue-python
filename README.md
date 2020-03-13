# Tripy

This project consists of a django app that provides the apis and a vuejs app that acts as SPA frontend

# Backend Setup
## setup flake8
create local git pre commit hook. This is a one time step
```bash
pre-commit install
```

## Install Dependencies
```bash
pip install -r requirements.txt
```

## Create env file
create the file .env inside tripy directory. Use .env.example as reference

## DB url
the database credentials are provided using a single string in the .env file
for mor information refer [this](https://github.com/jacobian/dj-database-url)

## Run migrations
```bash
cd tripy
python manage.py migrate
```

## Run The Server
```bash
cd tripy
python manage.py runserver
```

## Run The Django unit tests
```bash
cd tripy
python manage.py test
```

## running postman tests
For running the tests, make sure you start the api server with a test database

```bash
cd tripy
python manage.py runserver --settings=tripy.test_settings
```

```bash
cd postman_tests
npm run admin_flow.json -e env.json
```

# Web App setup
## go to web app director
```bash
cd webapp/tripy_web
```
## Project setup
```bash
yarn install
```

### Compiles and hot-reloads for development
```bash
yarn run serve
```

### Compiles and minifies for production
```bash
yarn run build
```
