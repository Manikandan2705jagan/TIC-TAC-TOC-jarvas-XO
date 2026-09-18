"""AI search algorithms for Tic-Tac-Toe.

Implements the classic Minimax algorithm both in its plain form and with
Alpha-Beta Pruning. The maximizer is always "X" and the minimizer is always
"O". Scores are returned from X's perspective so that:

    positive score -> X (AI/human) is winning
    negative score -> O is winning
    zero          -> draw

Scale: a win within `d` moves (depth) scores +/- (10 - d). This makes the AI
prefer winning as fast as possible and losing as slowly as possible.
"""

import tictactoe as ttt

INF = float("inf")


def _terminal_score(board, depth):
    win = ttt.winner(board)
    if win is ttt.PLAYER_X:
        return 10 - depth
    if win is ttt.PLAYER_O:
        return depth - 10
    return 0


def _new_stats():
    """Return a fresh stats dict used to count explored nodes."""
    return {"nodes": 0}


# ---------------------------------------------------------------------------
# Minimax (no pruning)
# ---------------------------------------------------------------------------

def minimax(board, player, depth=0, stats=None):
    """Plain minimax. Returns (best_score, best_move).

    `best_score` is from X's perspective. `best_move` is None at terminals.
    If `stats` is a dict, "nodes" is incremented for every node visited.
    """
    if stats is not None:
        stats["nodes"] += 1

    if ttt.is_terminal(board):
        return _terminal_score(board, depth), None

    if player == ttt.PLAYER_X:
        best_score = -INF
        best_move = None
        for move in ttt.available_moves(board):
            child = ttt.make_move(board, move, player)
            score, _ = minimax(child, ttt.other_player(player), depth + 1, stats)
            if score > best_score:
                best_score = score
                best_move = move
        return best_score, best_move

    best_score = INF
    best_move = None
    for move in ttt.available_moves(board):
        child = ttt.make_move(board, move, player)
        score, _ = minimax(child, ttt.other_player(player), depth + 1, stats)
        if score < best_score:
            best_score = score
            best_move = move
    return best_score, best_move


# ---------------------------------------------------------------------------
# Minimax with Alpha-Beta Pruning
# ---------------------------------------------------------------------------

def minimax_ab(board, player, alpha=-INF, beta=INF, depth=0, stats=None):
    """Minimax with alpha-beta pruning. Same return convention as `minimax`.

    `alpha`/`beta` are the best scores each side can currently guarantee.
    Branches that cannot improve on them are pruned.
    """
    if stats is not None:
        stats["nodes"] += 1

    if ttt.is_terminal(board):
        return _terminal_score(board, depth), None

    if player == ttt.PLAYER_X:
        best_score = -INF
        best_move = None
        for move in ttt.available_moves(board):
            child = ttt.make_move(board, move, player)
            score, _ = minimax_ab(child, ttt.other_player(player),
                                  alpha, beta, depth + 1, stats)
            if score > best_score:
                best_score = score
                best_move = move
            if best_score > alpha:
                alpha = best_score
            if beta <= alpha:
                break  # prune: O cannot improve this node
        return best_score, best_move

    best_score = INF
    best_move = None
    for move in ttt.available_moves(board):
        child = ttt.make_move(board, move, player)
        score, _ = minimax_ab(child, ttt.PLAYER_X,
                              alpha, beta, depth + 1, stats)
        if score < best_score:
            best_score = score
            best_move = move
        if best_score < beta:
            beta = best_score
        if beta <= alpha:
            break  # prune: X cannot improve this node
    return best_score, best_move


# ---------------------------------------------------------------------------
# Public interface
# ---------------------------------------------------------------------------

def best_move(board, ai_player, alpha_beta=True):
    """Return the strongest move (int 0-8) for `ai_player` on `board`.

    Uses alpha-beta pruning by default; set `alpha_beta=False` to use the
    plain minimax (useful for comparing search effort).
    """
    if ttt.is_terminal(board):
        raise ValueError("cannot choose a move on a finished board")

    search = minimax_ab if alpha_beta else minimax
    keyword_args = {}
    if alpha_beta:
        keyword_args = {"alpha": -INF, "beta": INF}

    _, move = search(board, ai_player, **keyword_args)
    return move


def compare_searches(board, ai_player):
    """Return a dict comparing plain vs pruned search on the same board.

    Keys: "plain_move", "plain_nodes", "pruned_move", "pruned_nodes".
    """
    plain_stats = _new_stats()
    pruned_stats = _new_stats()

    _, plain_move = minimax(board, ai_player, 0, plain_stats)
    _, pruned_move = minimax_ab(board, ai_player, -INF, INF, 0, pruned_stats)

    return {
        "plain_move": plain_move,
        "plain_nodes": plain_stats["nodes"],
        "pruned_move": pruned_move,
        "pruned_nodes": pruned_stats["nodes"],
    }