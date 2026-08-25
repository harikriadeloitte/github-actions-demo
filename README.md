# Action Board

A small Python task board for demonstrating GitHub Actions.

## Run locally

Requires Python 3.9 or newer:

```bash
python src/app.py
```

Open http://localhost:8000 in your browser. Tasks are kept in memory and reset when the app stops.

## Run checks

```bash
python -m unittest discover -s tests
```

The workflow in `.github/workflows/ci.yml` runs the test suite for pushes and pull requests.
