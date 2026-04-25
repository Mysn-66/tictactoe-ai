"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = 0
    o_count = 0

    for row in board:
        for cell in row:
            if cell == X:
                x_count += 1
            elif cell == O:
                o_count += 1

    return X if x_count == o_count else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    moves = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                moves.add((i, j))
    return moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action

    # Validate action bounds
    if i not in [0, 1, 2] or j not in [0, 1, 2]:
        raise Exception("Invalid action")

    # Cell must be empty
    if board[i][j] != EMPTY:
        raise Exception("Invalid move")

    new_board = copy.deepcopy(board)
    new_board[i][j] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Rows
    for i in range(3):
        if board[i][0] is not EMPTY and board[i][0] == board[i][1] == board[i][2]:
            return board[i][0]

    # Columns
    for j in range(3):
        if board[0][j] is not EMPTY and board[0][j] == board[1][j] == board[2][j]:
            return board[0][j]

    # Diagonals
    if board[0][0] is not EMPTY and board[0][0] == board[1][1] == board[2][2]:
        return board[0][0]

    if board[0][2] is not EMPTY and board[0][2] == board[1][1] == board[2][0]:
        return board[0][2]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True

    # If there is any empty cell, game is not over
    for row in board:
        if EMPTY in row:
            return False

    # No winner and no empty cells => tie
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    w = winner(board)
    if w == X:
        return 1
    if w == O:
        return -1
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    (Includes Alpha-Beta Pruning bonus optimization)
    """
    if terminal(board):
        return None

    turn = player(board)

    alpha = -math.inf
    beta = math.inf

    if turn == X:
        best_val = -math.inf
        best_action = None
        for action in actions(board):
            val = _min_value(result(board, action), alpha, beta)
            if val > best_val:
                best_val = val
                best_action = action
            alpha = max(alpha, best_val)
        return best_action
    else:
        best_val = math.inf
        best_action = None
        for action in actions(board):
            val = _max_value(result(board, action), alpha, beta)
            if val < best_val:
                best_val = val
                best_action = action
            beta = min(beta, best_val)
        return best_action


def _max_value(board, alpha, beta):
    if terminal(board):
        return utility(board)

    v = -math.inf
    for action in actions(board):
        v = max(v, _min_value(result(board, action), alpha, beta))
        alpha = max(alpha, v)
        if alpha >= beta:
            break  # prune
    return v


def _min_value(board, alpha, beta):
    if terminal(board):
        return utility(board)

    v = math.inf
    for action in actions(board):
        v = min(v, _max_value(result(board, action), alpha, beta))
        beta = min(beta, v)
        if alpha >= beta:
            break  # prune
    return v
