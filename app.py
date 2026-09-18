"""Flask web app for the Tic-Tac-Toe AI project (guest login only).

The minimax engine (`tictactoe.py` / `ai.py`) runs here and is exposed over
`/api/move` and `/api/compare`.

Configuration (environment variables, or `.env` file):
    SECRET_KEY   session signing key; set a random one in production
    HOST, PORT   override the default host/port
"""

import os

from dotenv import load_dotenv
from flask import (Flask, jsonify, redirect, render_template, request,
                   session, url_for)

import ai
import tictactoe as ttt

load_dotenv()

HOST = os.environ.get("HOST", "127.0.0.1")
PORT = int(os.environ.get("PORT", "5000"))
SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-change-me-in-production"

app = Flask(__name__)
app.secret_key = SECRET_KEY

SESSION_USER = "profile"
VALID_CELLS = (None, ttt.PLAYER_X, ttt.PLAYER_O)
VALID_PLAYERS = (ttt.PLAYER_X, ttt.PLAYER_O)


def current_user():
    return session.get(SESSION_USER)


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    if current_user() is None:
        return redirect(url_for("login"))
    return render_template("game.html", user=current_user())


@app.route("/login")
def login():
    if current_user() is not None:
        return redirect(url_for("index"))
    return render_template("login.html")


@app.route("/guest", methods=["POST"])
def auth_guest():
    session.clear()
    session[SESSION_USER] = {
        "name": "Guest",
        "email": "",
        "picture": "",
        "is_guest": True,
    }
    return jsonify({"ok": True, "user": session[SESSION_USER]})


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"ok": True})


# ---------------------------------------------------------------------------
# AI API
# ---------------------------------------------------------------------------

@app.route("/api/move", methods=["POST"])
def api_move():
    data = request.get_json(silent=True) or {}
    board = data.get("board")
    ai_player = data.get("ai_player", ttt.PLAYER_X)

    if not isinstance(board, list) or len(board) != 9:
        return jsonify({"error": "Board must be a list of 9 cells"}), 400
    if not all(cell in VALID_CELLS for cell in board):
        return jsonify({"error": "Invalid cell value"}), 400
    if ai_player not in VALID_PLAYERS:
        return jsonify({"error": "ai_player must be 'X' or 'O'"}), 400
    if ttt.is_terminal(board):
        return jsonify({"error": "Game is already over"}), 400

    move = ai.best_move(board, ai_player)
    stats = ai.compare_searches(board, ai_player)
    return jsonify({"move": move, "ai_player": ai_player, "stats": stats})


@app.route("/api/compare", methods=["POST"])
def api_compare():
    """Node-count comparison of plain minimax vs alpha-beta on a board."""
    data = request.get_json(silent=True) or {}
    board = data.get("board")
    if not isinstance(board, list) or len(board) != 9 or not all(
            cell in VALID_CELLS for cell in board):
        return jsonify({"error": "Board must be a list of 9 valid cells"}), 400
    stats = ai.compare_searches(board, ttt.PLAYER_X)
    return jsonify(stats)


if __name__ == "__main__":
    print("Tic-Tac-Toe AI running at http://%s:%d" % (HOST, PORT))
    app.run(host=HOST, port=PORT, debug=os.environ.get("FLASK_DEBUG") == "1")