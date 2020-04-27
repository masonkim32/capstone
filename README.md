# capstone: Casting Agency App

This app provide the functionality for creating movies and managing and
assigning actors to those movies. There are three roles with different
permissions like below:

- Casting Assistant
    - Can view actors and movies
- Casting Director
    - All permissions a Casting Assistant has and…
    - Add or delete an actor from the database
    - Modify actors or movies
- Executive Producer
    - All permissions a Casting Director has and…
    - Add or delete a movie from the database

## Casting Agency App on Heroku

This app is running on Heroku. The service root url is like below:

https://mason-kim-capstone.herokuapp.com

## Getting Started

### Prerequisites

- Python 3.6 or higher, and pip3
- Git, Postgresql, Postman, and Heroku Cli
- Using python virtual environment is highly recommended.

### Installation

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies
by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the
`requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

### Setup Database

Create castingagency database and user, then import initial data file
```database.sql``` from the project folder.

```
CREATE DATABASE castingagency;
GRANT ALL ON DATABASE castingagency to "castingagency";
ALTER USER castingagency PASSWORD 'development';
ALTER USER castingagency CREATEDB;

psql -U castingagency castingagency < database.sql
```

### Running the server

From the project directory, run:

```bash
FLASK_APP=api.py FLASK_ENV=development flask run
```


## Test your endpoints with [Postman](https://getpostman.com).

  - Before running postman test collection, database.sql must be imported to
castingagency database.
  - Import ```casting-agency-test-localhost.postman_collection.json``` from
```./postman_test``` folder.
  - Run the casting-agency-test collection and check every test is passed.


## API Reference.

### Getting Started

- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration.
- Authentication: This version of the application requires autho0 authentication. The application get JWT Token with proper permission from `masonkim32.eu.auth0.com`.

### GET /movies

- General: Retrieve a list of all movies from database.
- Action: GET
- URL: `http://127.0.0.1:5000/movies`

```
{
  "movies": [
    {
      "id": 1,
      "release_date": "Fri, 08 May 2020 00:00:00 GMT",
      "title": "The High Note"
    },
    {
      "id": 2,
      "release_date": "Fri, 17 Jul 2020 00:00:00 GMT",
      "title": "The Painted Bird"
    },
    {
      "id": 3,
      "release_date": "Fri, 24 Jul 2020 00:00:00 GMT",
      "title": "Mulan"
    },
    {
      "id": 4,
      "release_date": "Fri, 04 May 2012 00:00:00 GMT",
      "title": "The Avengers"
    },
    {
      "id": 5,
      "release_date": "Fri, 13 Feb 2004 00:00:00 GMT",
      "title": "City of God"
    },
    {
      "id": 6,
      "release_date": "Wed, 05 May 2004 00:00:00 GMT",
      "title": "Gladiator"
    },
    {
      "id": 7,
      "release_date": "Fri, 22 Dec 2023 00:00:00 GMT",
      "title": "Avatar3"
    },
    {
      "id": 8,
      "release_date": "Fri, 05 Aug 2022 00:00:00 GMT",
      "title": "Mission: Impossible 8"
    },
    {
      "id": 9,
      "release_date": "Fri, 08 Oct 2021 00:00:00 GMT",
      "title": "Uncharted"
    },
    {
      "id": 10,
      "release_date": "Wed, 31 Mar 1999 00:00:00 GMT",
      "title": "The Matrix "
    },
    {
      "id": 11,
      "release_date": "Fri, 24 Jul 1998 00:00:00 GMT",
      "title": "Saving Private Ryan"
    },
    {
      "id": 12,
      "release_date": "Wed, 06 Jul 1994 00:00:00 GMT",
      "title": "Forrest Gump"
    }
  ],
  "success": true
}
```

### GET /movie/<int:movie_id>

- General: Retrieve the movie data with provided id from database.
- Action: GET
- URL: `http://127.0.0.1:5000/movie/1`

```
{
  "movie": {
    "id": 1,
    "release_date": "Fri, 08 May 2020 00:00:00 GMT",
    "title": "The High Note"
  },
  "success": true
}
```

### POST /movie

- General: Add a new movie in the movies table when the request user have
    a proper permission.
- Action: POST
- URL: `http://127.0.0.1:5000/movie`
- Header: Content-Type: application/json
- Data(JSON): {"title": "New Movie", "release_date": "2022-04-04"}

```
{
  "created": 13,
  "success": true,
  "total_movies": 13
}
```

### PATCH /movie/<int:movie_id>

- General: Update the title or release_date of the movie with provided id. It
is permitted for users who have the proper validations.
- Action: PATCH
- URL: `http://127.0.0.1:5000/movie/13`
- Header: Content-Type: application/json
- Data(JSON): {"title": "Patched Movie", "release_date": "2022-04-05"}

```
{
  "movie": {
    "id": 13,
    "release_date": "Tue, 05 Apr 2022 00:00:00 GMT",
    "title": "Patched Movie"
  },
  "success": true
}
```

### DELETE /movie/<int:movie_id>

- General: Delete the corresponding row for movie_id. Only users with proper
permission can delete movie.
- Action: DELETE
- URL: `http://127.0.0.1:5000/movie/13`

```
{
  "deleted": 13,
  "success": true,
  "total_movies": 12
}
```

### GET /actors

- General: Retrieve a list of all actors from database.
- Action: GET
- URL: `http://127.0.0.1:5000/actors`

```
{
  "actors": [
    {
      "age": 83,
      "gender": "male",
      "id": 1,
      "name": "Morgan Freeman"
    },
    {
      "age": 46,
      "gender": "male",
      "id": 2,
      "name": "Leonardo DiCaprio"
    },
    {
      "age": 39,
      "gender": "female",
      "id": 3,
      "name": "Natalie Portman"
    },
    {
      "age": 38,
      "gender": "female",
      "id": 4,
      "name": "Anne Hathaway"
    },
    {
      "age": 77,
      "gender": "male",
      "id": 5,
      "name": "Robert De Niro"
    },
    {
      "age": 74,
      "gender": "female",
      "id": 6,
      "name": "Diane Keaton"
    },
    {
      "age": 35,
      "gender": "female",
      "id": 7,
      "name": "Keira Knightley"
    },
    {
      "age": 44,
      "gender": "male",
      "id": 8,
      "name": "Cillian Murphy"
    },
    {
      "age": 83,
      "gender": "male",
      "id": 9,
      "name": "Jack Nicholson"
    },
    {
      "age": 43,
      "gender": "male",
      "id": 10,
      "name": "Tom Hardy"
    },
    {
      "age": 53,
      "gender": "male",
      "id": 11,
      "name": "Mark Ruffalo"
    },
    {
      "age": 22,
      "gender": "female",
      "id": 12,
      "name": "Elle Fanning"
    },
    {
      "age": 36,
      "gender": "female",
      "id": 13,
      "name": "Scarlett Johansson"
    }
  ],
  "success": true
}
```

### GET /actor/<int:actor_id>

- General: Retrieve the actor data with provided id from database.
- Action: GET
- URL: `http://127.0.0.1:5000/actor/1`

```
{
  "actor": {
    "age": 83,
    "gender": "male",
    "id": 1,
    "name": "Morgan Freeman"
  },
  "success": true
}
```

### POST /actor

- General: Add a new actor in the actors table when the request user have
a proper permission.
- Action: POST
- URL: `http://127.0.0.1:5000/actor`
- Header: Content-Type: application/json
- Data(JSON): {"name": "New actor", "age": 20, "gender": "male"}

```
{
  "created": 14,
  "success": true,
  "total_actors": 14
}
```

### PATCH /actor/<int:actor_id>

- General: Update the name, age, or gender of the actor with provided id. It is
permitted for users who have the proper validations.
- Action: PATCH
- URL: `http://127.0.0.1:5000/actor/14`
- Header: Content-Type: application/json
- Data(JSON): {"name": "Patched actor", "age": 20, "gender": "female"}

```
{
  "actor": {
    "age": 20,
    "gender": "female",
    "id": 14,
    "name": "Patched actor"
  },
  "success": true
}
```

### DELETE /actor/<int:actor_id>

- General: Delete the corresponding row for actor_id. Only users with proper
permission can delete movie.
- Action: DELETE
- URL: `http://127.0.0.1:5000/actor/14`

```
{
  "deleted": 14,
  "success": true,
  "total_actors": 13
}
```

### Error Handling

- Errors are returned as JSON objects

```
{
    "success": False,
    "error": 400,
    "message": "bad request"
}
```

- 400: Bad request
- 401: Not authorized
- 404: Resource is not found
- 405: Method not allowed
- 422: Unprocessable


## Authors

- Mason Myoungsung Kim
- Start Code provided by Udacity Team
