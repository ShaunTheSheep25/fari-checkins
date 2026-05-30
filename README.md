# Fari - Daily Eldercare Checkin RestAPI

Hey! This is a simple RestAPI that I built, modeled after the robot Fari, which is used as an AI-aided assistive eldercare companion. It is modeled based on Fari's daily check-in behaviour, and can serve as a feasible companion-app backend. It is constructed off a "Resident - Caregiver - Checkin" data model (depicted in /docs/erd.png), and supports basic CRUD (Create/Read/Update/Delete) operations via FastAPI endpoints, along with endpoints to get "n" checkins for each resident + summarize said daily checkins. I've also included a testing script (implemented with pytest) for each endpoint's happy path, and I've accounted for multiple types of failure paths (ValidationError, 404 Not Found etc). The instructions to run the same (and a few other details) have been included below.

(Do note that you must have Git and Python 3.11+ downloaded on your system before you can run these commands)

## How to run it

1. Clone the repo using git clone

```bash
git clone https://github.com/ShaunTheSheep25/fari-checkins.git
cd fari-checkins
```

Note: If you're using pyenv, set up the environment first:
```bash
pyenv virtualenv 3.11 fari-checkins
pyenv local fari-checkins
```

2. Install dependencies with pip (taken care of in the pyproject.toml file)

```bash
pip install -e ".[dev]"
```

3. Run the server using uvicorn

```bash
uvicorn fari_checkins.main:app --reload
```

4. Visit the link `http://127.0.0.1:8000/docs` on your browser, for the interactive documentation available on Swagger UI to test each endpoint of the RestAPI.

## How to test it

To test the RestAPI, you can run pytest with or without coverage, depending on the level of detail you'd want in the final report.

```bash
pytest tests/                   # simple testing, no coverage
pytest --cov=src tests/         # miss-rate coverage of testing script
```

## Limitations + What I'd do next

There are a few limitations I've come across while implemting this RestAPI -

- Endpoints roughly cover ~85% of the test cases implemented by the testing script. While this crosses the 70% boundary check for said project, when implementing these on a large scale, each edge case must be taken care of to increase the overall coverage(specifically with the 'database.py' error handling setup) along with pagination for list endpoints
- SQLite isn't suitable for production on a mass scale. In the future, I'd consider switching to alternate Database Management Systems like PostgreSQL, Oracle DBMS etc. in a more professional environment
- I've implemented the caregiver endpoints such that each "caregiver" here is tied to a single resident, which suffices for now, but later on I'll definitely look into creating a "many-one" system with respect to the caregiver and residents (i.e, multiple residents being taken care of by a single caregiver)
- No authentication system has been implemented as of yet, so I'll be looking into doing that soon using JWT authentication (with python-jose and passlib)



