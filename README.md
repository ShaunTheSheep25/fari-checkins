# My Toolkit

Hey! This is a simple toolkit that I developed that runs a linter and typecheck through the code you push to a repo (here I've also implemented a simple FastAPI "Hello, world!" endpoint along with a testing script for it). I've also created a pyproject.toml file that takes care of the dependencies required to run this project on any computer - fastapi, uvicorn etc, along with 3 tools (ruff, black and mypy) that I've wired in as pre-commit hooks to check your code for redundancy and innacuracy. 

(Do note that you must have Git and Python 3.11+ downloaded on your system before you can run these commands)

The commands to clone this repo and have the "Hello, world!" endpoint running are as follows -

1. Clone the repo using git clone

```
git clone https://github.com/ShaunTheSheep25/shaun-toolkit.git
cd shaun-toolkit
```

2. Install dependencies with pip (taken care of in the pyproject.toml file)

```
pip install -e ".[dev]"
```

3. Run the server using uvicorn

```
uvicorn toolkit.main:app --reload
```

4. Visit the link http://127.0.0.1:8000/hello on your browser. You should see a json object displayed as {"message": "Hello, world!"}.

5. (Optional, not required) Run the testing script for the FastAPI endpoint

```
pytest tests/
```

And that's pretty much it! Hope this comes in handy for wherever you need a testing toolkit before you push files to a repo.