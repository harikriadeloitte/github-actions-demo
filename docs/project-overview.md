# Project Overview

## Application Logic

The Action Board is a small Python web application served by `src/app.py` at `http://localhost:8000`.

Tasks are stored in the in-memory `TASKS` list. Each task has an `id`, a `title`, and a `done` status.

The application supports three operations:

- **Add:** trims the title, ignores blank titles, and assigns the next available ID.
- **Toggle:** switches a task between complete and incomplete.
- **Remove:** deletes a task by ID.

The task list resets whenever the application stops because no database or file storage is used.

## Test Cases

The tests are in `tests/test_app.py`. The `setUp()` method creates a fresh task list before every test.

1. `test_add_task_trims_title` verifies that surrounding spaces are removed from a task title.
2. `test_add_task_assigns_next_id` verifies that a new task receives the next ID and starts incomplete.
3. `test_blank_task_is_ignored` verifies that whitespace-only titles do not create tasks.
4. `test_toggle_task` verifies that an incomplete task can be marked complete.
5. `test_remove_task` verifies that a task can be deleted.

Run the tests locally with:

```powershell
python -m unittest discover -s tests
```

## Continuous Integration

The workflow in `.github/workflows/ci.yml` runs for every push and pull request. It checks out the repository, installs Python 3.12, and runs the test suite.

A successful workflow confirms that the five automated tests pass in a clean GitHub Actions environment.
