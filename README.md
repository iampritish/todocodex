# TodoCodex

A full-stack todo application built with Flask, SQLite, and a lightweight HTML/CSS/JS frontend.

## Features
- Create, list, update, and delete todos via a REST API.
- Mark todos as completed and edit titles in-place.
- Minimal dark-themed interface with instant updates.

## Quickstart
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the server:
   ```bash
   flask --app app run --debug
   ```
   The app listens on `http://127.0.0.1:5000`.

## Running tests
```bash
pytest
```

## Configuration
- `TODO_DATABASE`: Optional environment variable to override the SQLite database path (default `todo.db`).
