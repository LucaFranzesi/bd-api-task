# [bd-task] - Implementing an API for mockup data fetching

## Introduction

This repository implements an application for serving a REST API for mockup data of users and todos offered by a third party API ([JSON placeholder ](https://jsonplaceholder.typicode.com/)).

All endpoints are exposed in GET method.

The API exposes two endpoints reachable from localhost on port 8000, with parameters passed as query string (this choice is motivated by parameters simplicity, with no complex structure and a limited number of parameters):

- **'/users'**  : Returns a list of users with their attributes, fetched from https://jsonplaceholder.typicode.com/users and allows to paginate them with two query parameters: limit and offset (by default set as 5 and 0).

- **'/todos'**  : Returns a list of todos with their attributes for a specific user, fetched from https://jsonplaceholder.typicode.com/todos passing the userIs as a required query parameter and allows to paginate them with other two query parameters: limit and offset (by default set as 5 and 0).

Along with those endpoint, the API exposes another one for testing purposes and a swagger for interacting with the endpoints:

- **'/db_logs'** : Returns a list of all HTTP Request logs saved on a SQL Database. This endpoint can use two query parameters to paginate results provided: limit and offset (by default set as 10 and 0).
- **'/docs'** : Returns a Swagger where it wil be possible to interact with developed endpoints

The API provides a set of unit test inside the folder /tests. Those tests can be triggered inside the project with `>> pytest`. 

**NOTE:** The applications need a SQL database to be correctly run and tested. Follow the **Quickstart** section to understand all of different ways to run the application.

The application has been developed in Python v3.12.1 but has been automatically tested for versions 3.9, 3.10, 3.11, 3.12. 

**NOTE:** This test is implemented through a Github Action, eventually replaced with test on containers when containerization has been implemented.

## Technologies

The application utilizes Python's FastAPI to set and manage all the endpoints and middleware, this technology has been chosen for its development simplicity, its execution speed and great solidity provided.

We have three main components developed in python:
- main => containing the endpoints and middleware provided by **FastAPI**
- tests => containing application unit tests, accessible with **pytest**
- orm model => containing SQL database (tables and attributes) model, implemented with **sqlalchemy**

Other technologies utilized are:
- Docker (and docker-compose) to allow database and application containerization in a secure and os-independent way.
- Postgres SQL as a SQL Server, containing our database and an history of HTTP requests received by our application
- Github Actions to provide a basic example of CI possibilities and automatic testing in case of pull requests on main branch
- Swagger as a web tool to interact with our API calls

## Quickstart

The application is developed in two different stages:

- The first one includes a classic python API without any SQL database for logging (Variant A)
- The second one introduces a SQL database as a docker container and allows to run the application through a docker container (Variant B)
On the next paragraphs it will be explained how to run all the different variants.

### (Variant A)

First of all you should clone the package in a local environment through `git clone`. The project structure will be displayed as:

```
bd-task/
├── src/
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── todo_test.py
│   │   ├── user_test.py
│   ├── __init__.py
│   ├── main.py
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
├── setup.py
```
From inside the project folder you can setup and run the application:

- Before running the application you will need to install requirements with `pip install -r requirements.txt` 
- You can run automatic tests using the command `pytest` before running the application to check for its correctness
- The application can be run in development mode with the command `fastapi dev ./src/main.py`

This will start a server exposing the applications' endpoint and a Swagger to test them through a simple interface.

The Swagger can beh reached from http://localhost:8000/docs and will present the two endpoints previously described.

You can test them through "Try It Out" or you can use other tools like curl or Postman.

At this point only /users and /todos endpoint are exposed.

You can filter returned values by passing three possible query parameters:
- limit : int -> limit the number of result returned (default 5). If there are less results than limit imposed all results will be returned
- offset : int -> declares the starting point where result will be shown (default 0).

Offset and limit are used togheter to provide result pagination.

- userId (todos only) : int -> a required parameter to filter todos for a specific user. If the user does not exist, 0 results will be provided.

### (Variant B)

First of all you should clone the package in a local environment through `git clone`. The project structure will be displayed as:

```
my_project/
├── db/
│   ├── docker-compose.yaml
├── src/
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── todo_test.py
│   │   ├── user_test.py
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
├── .gitignore
├── Dockerfile
├── LICENSE
├── README.md
├── docker-compose.yaml
├── requirements.txt
├── setup.py
```

This version allows to create a Postgres SQL database to store a log of HTTP requests and let the user choose between containerizing the python application or using it in a classic way.

Before running the application in traditional way the SQL container must be initialized with `docker-compose up -d` from inside the db folder.

Our SQL Server will be exposed on port 5432 and can be accessed with `docker exec -it fastapi_db psql -U lucaf -d http_db`. Inside the container you can query the database with SQL in a command line environment.

To run and test the application in a traditional way, please refer to **Variant A**.

To run the application in a docker container you just need to initialize the components declared inside of the docker-compose located in the project folder `docker-compose up -d`.

You can check the correct initialization with `docker-compose ps` where you should expect to find two processes named fastapi_app and fastapi_db running.

You can check for a correct application execution by running unit tests inside the container with `docker-compose exec web pytest ./src/tests`.

The endpoints will be reachable at the same condition described at **Variant A**

## Notes

To prevent a wrong push on main, a branch protection rule has been applied, where a user cannot directly push/merge on main, but needs to pass for a pull request where some Github Actions will be preliminary performed.

For **Variant A** a Github Action will perform unit tests on different versions of python to ensure a minimum of retro-compatibility for the application.

For **Variant B** a new Action is created to automatically deploy containers and running the unit tests inside of them and the original Action is updated to complete