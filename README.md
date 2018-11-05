# star-wars-planets-api
Basic Star Wars Planets API for insertion, removal and querying.

## Requirements

* MongoDB
* Python 3
  - flask
  - flask-restful
  - pytest

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

* Validate input data for HTTP requests and database operations
* Change to a BDD tool for testing (e.g.: behave)
* Integrate the code with a CI tool for testing (Travis, Jenkins, etc.)
* Document all methods
* Schedule a job for updating films count for planets in the database (make it
  future-proof for when a new film is released)
