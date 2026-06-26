import math
import random

def check_win(board, player):
    win_states = [
        (0,1,2), (3,4,5), (6,7,8), # Hàng ngang
        (0,3,6), (1,4,7), (2,5,8), # Hàng dọc
        (0,4,8), (2,4,6)           # Chéo
    ]
    for state in win_states:
        if board[state[0]] == board[state[1]] == board[state[2]] == player:
            return True
    return False

def check_draw(board):
    return ' ' not in board

def evaluate(board):
    if check_win(board, 'X'): return 10
    if check_win(board, 'O'): return -10
    return 0

def get_empty_cells(board):
    return [i for i, x in enumerate(board) if x == ' ']

# Thuật toán Minimax
def minimax(board, depth, is_max):
    score = evaluate(board)
    if score == 10: return score - depth
    if score == -10: return score + depth
    if check_draw(board): return 0
    empty_cells = get_empty_cells(board)
    if is_max:
        best = -math.inf
        for i in empty_cells:
            board[i] = 'X'
            best = max(best, minimax(board, depth + 1, False))
            board[i] = ' '
        return best
    else:
        best = math.inf
        for i in empty_cells:
            board[i] = 'O'
            best = min(best, minimax(board, depth + 1, True))
            board[i] = ' '
        return best

# Thuật toán Alpha-Beta Pruning
def alpha_beta(board, depth, alpha, beta, is_max):
    score = evaluate(board)
    if score == 10: return score - depth
    if score == -10: return score + depth
    if check_draw(board): return 0
    empty_cells = get_empty_cells(board)
    if is_max:
        best = -math.inf
        for i in empty_cells:
            board[i] = 'X'
            best = max(best, alpha_beta(board, depth + 1, alpha, beta, False))
            board[i] = ' '
            alpha = max(alpha, best)
            if beta <= alpha: break
        return best
    else:
        best = math.inf
        for i in empty_cells:
            board[i] = 'O'
            best = min(best, alpha_beta(board, depth + 1, alpha, beta, True))
            board[i] = ' '
            beta = min(beta, best)
            if beta <= alpha: break
        return best

# Thuật toán Expectimax
def expectimax(board, depth, is_max):
    score = evaluate(board)
    if score == 10: return score - depth
    if score == -10: return score + depth
    if check_draw(board): return 0
    empty_cells = get_empty_cells(board)
    if is_max:
        best = -math.inf
        for i in empty_cells:
            board[i] = 'X'
            best = max(best, expectimax(board, depth + 1, False))
            board[i] = ' '
        return best
    else:
        # Nút xác suất cho O, giả sử đối thủ đi ngẫu nhiên
        expected_value = 0
        for i in empty_cells:
            board[i] = 'O'
            expected_value += expectimax(board, depth + 1, True)
            board[i] = ' '
        return expected_value / len(empty_cells)

# Hàm lấy nước đi tốt nhất cho AI
def get_best_move(board, algo, ai_player):
    empty_cells = get_empty_cells(board)
    if len(empty_cells) == 9:
        return random.choice([0, 2, 4, 6, 8])
    best_val = -math.inf if ai_player == 'X' else math.inf
    best_move = -1
    is_next_max = (ai_player == 'O')
    for i in empty_cells:
        board[i] = ai_player
        if algo == "Minimax":
            move_val = minimax(board, 0, is_next_max)
        elif algo == "Alpha-Beta":
            move_val = alpha_beta(board, 0, -math.inf, math.inf, is_next_max)
        elif algo == "Expectimax":
            move_val = expectimax(board, 0, is_next_max)
        board[i] = ' '
        if ai_player == 'X': # AI tìm max
            if move_val > best_val:
                best_val = move_val
                best_move = i
        else: # AI tìm min
            if move_val < best_val:
                best_val = move_val
                best_move = i
    return best_move