# Casting Agency FSND

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Mysql

Follow instructions to install the latest version of mysql for your platform in the [mysql docs](https://dev.mysql.com/doc/mysql-installation-excerpt/5.7/en/)


## Install dependencies of mysql for python

- `sudo apt-get install python-mysqldb`
- `sudo apt-get install python3.7-dev libmysqlclient-dev`


#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.


##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.


## Database Setup
With Mysql running, restore a database using the agency.sql file provided. From the backend folder in terminal run:
```bash
mysql agency < agency.sql
```

## Running the server

From within the project directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
export SQLALCHEMY_DATABASE_URI=mysql://admin:admin@localhost/agency
flask run
```
The `--reload` flag will detect file changes and restart the server automatically.

## Casting Agency Specifications
##### The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

#### Models
- Movies with attributes title and release date
- Actors with attributes name, age and gender

#### Endpoints
- GET /actors and /movies
- DELETE /actors/ and /movies/
- POST /actors and /movies and
- PATCH /actors/ and /movies/


##Roles
#### Casting Assistant
- Can view actors and movies

#### Casting Director
- All permissions a Casting Assistant has and…
- Add or delete an actor from the database
- Modify actors or movies

#### Executive Producer
- All permissions a Casting Director has
- Add or delete a movie from the database

## Testing
- One test for success behavior of each endpoint
- One test for error behavior of each endpoint
- At least two tests of RBAC for each role

To run the tests, run
```
python test_flaskr.py
```

## API status code
###200 (OK)
- Response json `{"success": true}`

###400 (Bad Request)
- Response json `{"success": False,"error": 400,"message": " Bad Request"})`

###404 (not found)
- Response json `{
            "success": False,
            "error": 404,
            "message": "not found"
        })`

###401 (Unauthorized)
- Response json `{
            "success": False,
            "error": 500,
            "message": "Token expired |Authorization malformed | Permission not found in JWT |JWT not found
        }`

###422 (unprocessable)
- Response json `{
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }`

###500 (Internal Server Error)
- Response json `{"success": False,  "error": 500,  "message": "Internal Server Error" }`
        
       
##Endpoint APi Request and Response


Endpoints GET `'/actors' ` To  fetches all available actors
- headers={'Authorization': 'Bearer {JWT}'}
- Response Example
```
{
"actors": [
  {
"age": 83,
"gender": "M",
"id": 1,
"name": "Morgan Freeman"
}
],
"success": true
}

```

Endpoints POST `'/actors' ` To  crete  new actor
- headers={'Authorization': 'Bearer {JWT}'}
- Request json Example
```
{
"age": 83,
"gender": "M",
"name": "Morgan Freeman"
}
```
- Response Example
```
{
"actor": {
"age": 83,
"gender": "M",
"id": 2,
"name": "Morgan Freeman"
},
"success": true
}
```

Endpoints PATCH `'/actors/{actor_id}' ` To  update an actor
- headers={'Authorization': 'Bearer {JWT}'}
- Request json Example
```
{
"age": 84,
"gender": "M",
"name": "Morgan Freeman"
}
```
- Response Example
```
{
"id": 2,
"success": true
}
```

Endpoints DELETE `'/actors/{actor_id}' ` To  delete an actor
- headers={'Authorization': 'Bearer {JWT}'}
- Response Example
```
{
"deleted_id": 2,
"success": true
}
```
Endpoints GET `'/movies' ` To  fetches all available movies
- headers={'Authorization': 'Bearer {JWT}'}
- Response Example
```
{
"movies": [
  {
"id": 1,
"release": "2020-07-01",
"title": "My spy"
}
],
"success": true
}

```

Endpoints POST `'/movies' ` To  crete  new movie
- headers={'Authorization': 'Bearer {JWT}'}
- Request json Example
```
{
"title": "My spy",
"release": "2020-07-01"
}
```
- Response Example
```
{
"movie": {
"id": 2,
"release": "2020-07-01",
"title": "My spy"
},
"success": true
}
```

Endpoints PATCH `'/movies/{movie_id}' ` To  update a movie
- headers={'Authorization': 'Bearer {JWT}'}
- Request json Example
```
{
"release": "2020-07-01",
"title": "My spy 2"
}
```
- Response Example
```
{
"movie_id": 2,
"success": true
}
```

Endpoints DELETE `'/actors/{movie_id}' ` To  delete a movie
- headers={'Authorization': 'Bearer {JWT}'}
- Response Example
```
{
"movie_id": 2,
"success": true
}
```