# star-wars-planets-api
Basic Star Wars Planets RESTful API for insertion, removal and querying of the Star
Wars saga's planets.

## Requirements

* MongoDB
* Python 3
  - flask
  - flask-restful
  - pytest

## API

* `/planets`
  - `GET`: List all planets
  - `PUT`: Insert a new planet data, containing name, terrain and climate in JSON
  format
* `/planets/<planet_id>`
  - `GET`: Retrieve a single planet data by its unique ID.
  - `DELETE`: Delete a planet by its unique ID.
* `/planets/name/<planet_name>`
  - `GET`: Retrieve a single planet data by its name.

## Executing

In the root directory, run:

```bash
python3 app.py
```

## Testing

In the root directory, run:

```bash
python3 -m pytest
```

## To-dos

* Document the API and use a tool to generate its documentation
* Validate input data for HTTP requests and database operations
* Change to a BDD tool for testing (e.g.: behave)
* Add coverage tests
* Integrate the code with a CI tool for testing (Travis, Jenkins, etc.)
* Document all methods
* Schedule a job for updating films count for planets in the database (make it
  future-proof for when a new film is released)
