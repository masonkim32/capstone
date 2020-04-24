# capstone


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

### GET /movie/1

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

{
	"title": "New Movie",
	"release_date": "2022-04-04"
}

```
{
  "created": 13,
  "success": true,
  "total_movies": 13
}
```

### PATCH /movie/13

{
	"title": "Patched Movie",
	"release_date": "2022-04-05"
}

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

### DELETE /movie/13

```
{
  "deleted": 13,
  "success": true,
  "total_movies": 12
}
```


### GET /actors

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


### GET /actor/1

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
{
    "name": "New actor"
    "age": 20,
    "gender": "male",
}

```
{
  "created": 14,
  "success": true,
  "total_actors": 14
}
```

### PATCH /actor/14
{
    "name": "Patched actor"
    "age": 20,
    "gender": "female",
}

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

### DELETE /actor/14

```
{
  "deleted": 14,
  "success": true,
  "total_actors": 13
}
```