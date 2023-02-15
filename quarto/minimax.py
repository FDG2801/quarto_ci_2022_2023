from copy import deepcopy
import random
import itertools

EVAL_TIE = 0  # this draw value only matters in the endgame, where the heuristic doesn't matter anymore
EVAL_WIN = 1 
MAX_DEPTH = 4

'''
TODO:
- game_state must be adapted with the professor's code OK
- test OK
- add heuristics (?) to choose piece/to place the piece


high=piece_val & 0b1000
coloured=piece_val & 0b0100
solid=piece_val & 0b0010
square=piece_val & 0b0001
'''

def minmax(game, depth, maximizingPlayer, chosenPiece=None, alpha=-float('inf'), beta=float('inf')):
    # Base case: return the score if the game is over or the depth limit has been reached
    if depth == 0 or game.check_winner() != -1:
        return state_eval(game, depth, maximizingPlayer)
    # Recursive case: try all possible moves and choose the best one
    if maximizingPlayer:
        best_value = -float('inf')
        for move,piece in itertools.product(get_all_possible_moves(game),list(set(range(16)) - set(game._board.ravel()))):
                game_t = deepcopy(game)
                game_t.place(move[0], move[1])
                game_t.select(piece)
                result = minmax(game_t, depth - 1, False , alpha, beta)
                best_value = max(best_value, result)
                alpha = max(alpha, best_value)
                if beta <= alpha:
                    break
            #else:
        return best_value
            #break
    else:
        best_value = float('inf')
        for move,piece in itertools.product(get_all_possible_moves(game),list(set(range(16)) - set(game._board.ravel()))):
                game_t = deepcopy(game)
                game_t.place(move[0], move[1])
                game_t.select(piece)
                result = minmax(game_t, depth - 1, True , alpha, beta)
                best_value = min(best_value, result)
                beta = min(beta, best_value)
                if beta <= alpha:
                    break
            #else:
        return best_value
            #break

def play(game, depth):
    scored_moves = []
    for move in get_all_possible_moves(game):
        game_t = deepcopy(game)
        game_t.place(move[0], move[1])
        scored_moves.append((move, minmax(game_t, depth, False)))
    scored_moves.sort(key=lambda x: x[1], reverse=True)
    scored_moves = list(filter(lambda x: x[1] != -1, scored_moves))
    #print(scored_moves)
    return scored_moves[0][0] if scored_moves[0][1] != float('-inf') or  scored_moves[0][1] != -1 else None #if scored_moves[0][1] != float('-inf') or  scored_moves[0][1] != -1 else None #[REMOVED CONDITION] scored_moves[0][1] != float('-inf') or
    

def choose_piece(game):
    piece_ok = False
    while not piece_ok:
        piece_ok = game.select(random.randint(0,15))
    return True

# get list of valid moves
def get_all_possible_moves(game_state):
    list = []
    board = game_state.get_board_status()
    for i in range(4):
        for j in range(4):
            if board[i][j] == -1:
                list.append((j, i))
    return list

def state_eval(game_state, depth, is_maximizing):
    '''
    Computes the evaluation of the state of the game
    '''
    if game_state.check_winner() != -1:
        return -float('inf') if is_maximizing else EVAL_WIN + depth
    elif game_state.check_finished:
        return 0
    else:
        return -1
