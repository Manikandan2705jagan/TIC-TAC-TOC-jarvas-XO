"""Play Tic-Tac-Toe against an unbeatable AI in your terminal.

The AI uses Minimax with Alpha-Beta Pruning. It never loses: every game ends
in a draw (or an AI win if the human blunders).
"""

import tictactoe as ttt
import ai

MENU = """TIC-TAC-TOE AI
1. Play as X (you move first)
2. Play as O (AI moves first)
3. Compare Minimax vs Alpha-Beta search effort
4. Quit
"""


def get_human_move(board):
    while True:
        try:
            choice = int(input("Your move (0-8): "))
        except ValueError:
            print("Please enter a number between 0 and 8.")
            continue
        if choice not in ttt.available_moves(board):
            print("That cell is taken or invalid. Try again.")
            continue
        return choice


def play_game(human_player):
    board = ttt.empty_board()
    ai_player = ttt.other_player(human_player)
    current = ttt.PLAYER_X

    while not ttt.is_terminal(board):
        print()
        print(ttt.render(board))
        print()

        if current == human_player:
            move = get_human_move(board)
        else:
            move = ai.best_move(board, ai_player)
            print(f"AI ({ai_player}) plays {move}")

        board = ttt.make_move(board, move, current)
        current = ttt.other_player(current)

    print()
    print(ttt.render(board))
    print()

    win = ttt.winner(board)
    if win is None:
        print("It's a draw. The AI is unbeatable!")
    elif win == human_player:
        print("You win! (The AI suggests this shouldn't happen.)")
    else:
        print(f"AI ({win}) wins. Unlucky!")


def compare_mode():
    board = ttt.empty_board()
    print("Comparing the two searches from the empty board (AI = X):")
    result = ai.compare_searches(board, ttt.PLAYER_X)
    print(f"  Plain minimax      : move={result['plain_move']}, "
          f"nodes explored={result['plain_nodes']}")
    print(f"  With alpha-beta    : move={result['pruned_move']}, "
          f"nodes explored={result['pruned_nodes']}")
    saved = result["plain_nodes"] - result["pruned_nodes"]
    pct = saved / result["plain_nodes"] * 100 if result["plain_nodes"] else 0
    print(f"  Nodes saved        : {saved} ({pct:.1f}%)")


def main():
    while True:
        print(MENU)
        choice = input("> ").strip()
        if choice == "1":
            play_game(ttt.PLAYER_X)
        elif choice == "2":
            play_game(ttt.PLAYER_O)
        elif choice == "3":
            compare_mode()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()