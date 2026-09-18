# Tic-Tac-Toe AI

A Flask web game and terminal application for playing Tic-Tac-Toe against an unbeatable AI. The AI uses Minimax with Alpha-Beta pruning and includes a comparison of both search strategies.

## Features

- Play in the browser as X or O.
- Guest login with session-based state.
- Unbeatable Minimax AI.
- Plain Minimax versus Alpha-Beta node-count comparison.
- Terminal game mode.
- Automated unit tests for game logic and AI behavior.

## Requirements

- Python 3.10 or newer

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Optionally create a local configuration file:

```powershell
Copy-Item .env.example .env
```

Set a random `SECRET_KEY` in `.env` before deploying outside local development.

## Run the web app

```powershell
python app.py
```

Open http://127.0.0.1:5000 in a browser.

## Run the terminal app

```powershell
python main.py
```

## Run tests

```powershell
python -m unittest test_ai -v
```

## Project structure

```text
app.py              Flask web server and JSON API
ai.py               Minimax and Alpha-Beta search implementation
tictactoe.py        Board rules and game-state helpers
main.py             Terminal game interface
test_ai.py          Unit tests
templates/          Flask HTML templates
static/             Browser JavaScript and CSS
```

## API endpoints

- `POST /guest` starts a guest session.
- `POST /logout` ends the current session.
- `POST /api/move` returns the AI move and search statistics.
- `POST /api/compare` compares plain Minimax and Alpha-Beta search.
