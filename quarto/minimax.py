from copy import deepcopy
import random

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


### BACKUP 1
# def minimax(quarto,depth:int,max_player:bool, chosen_piece, alpha=float('-inf'),beta=float('inf')):
#     game_state=deepcopy(quarto)
#     '''
#     game=self.get_game() -> Quarto type (adapted)
#     board=game.get_board_status() -> ndarray (adapted)

#     ORIGINAL 
#     game_state -- a tuple of three elements :
#         - [0] the game_board
#         - [1] the storage_board, a Board object that holds the pieces available to pick --- ???
#         - [2] the selected_piece coordinates, a tuple of (x, y) coordinates that correspond to an available piece
#         on the storage_board. This is the piece that has to be put on the game_board.
#     depth -- int that represents the maximum depth we will explore
#     max_player -- the player trying to maximize its evaluation, True if maximizing, False if minimizing
#     alpha -- initialized to the worst possible evaluation, has to be None if we don't want any pruning
#     beta -- initialized to the best possible evaluation, has to be None if we don't want any pruning
#     Returns
#     a tuple that contains :
#     [0] the evaluation of the child (between -9 for a loss, and 9 for a win)
#     [1] the new game_state
#     '''
#     game=game_state.get_game()
#     board=game_state.get_board_status() #ndarray
#     #Terminal state or max depth reached
#     if depth==0 or game.check_winner():
#         return state_eval(game)*(-1 if max_player else 1) # return the evaluation of the child and the child itself
#     best_move=None #there are no more moves

#     if max_player:
#         max_eval=float('-inf')
#         for child in get_all_possible_states(game_state): #get all the free positions -> get_all_possible_moves
#             evaluation=minimax(child, depth-1, False, chosen_piece, alpha,beta)[0] #the evaluation child is at index 0 -> pass the chosen piece
#             max_eval=max(max_eval,evaluation)
#             if max_eval==evaluation:
#                 best_move=child 
#             #alpha-beta pruning
#             if alpha and beta:
#                 alpha=max(alpha,max_eval)
#                 if beta<=alpha: #better options available
#                     break
#         return max_eval,best_move
#     #minimize the evaluation
#     else:
#         min_eval=float('inf')
#         for child in get_all_possible_states(game_state): #get all the free positions -> get_all_possible_moves
#             evaluation=minimax(child, depth-1, True, chosen_piece, alpha,beta)[0] #the evaluation child is at index 0 -> pass the chosen piece
#             min_eval=min(min_eval,evaluation)
#             if min_eval==evaluation:
#                 best_move=child 
#             #alpha-beta pruning
#             if alpha and beta:
#                 beta=min(beta,min_eval)
#                 if beta<=alpha: #better options available
#                     break
#         return min_eval,best_move 
# ------------------------------------------------------------------------------------------------------------------------------ #
def minimax_function(game, depth, maximizingPlayer, chosenPiece=None, alpha=-float('inf'), beta=float('inf')):
    # Base case: return the score if the game is over or the depth limit has been reached
    if depth == 0:
        return state_eval(game)

    # Recursive case: try all possible moves and choose the best one
    if maximizingPlayer:
        bestValue = -float('inf')
        for move in get_all_possible_moves(game):
            game_t = deepcopy(game)
            piece = choose_piece(game_t)
            game.place(move[0], move[1])
            result = minimax_function(game_t, depth - 1, False, piece , alpha, beta)
            bestValue = max(bestValue, result)
            alpha = max(alpha, bestValue)
            if beta <= alpha:
                break
        return bestValue
    else:
        bestValue = float('inf')
        for move in get_all_possible_moves(game):
            game_t = deepcopy(game)
            piece = choose_piece(game_t)
            game_t.place(move[0], move[1])
            result = minimax_function(game_t, depth - 1, True, piece , alpha, beta)
            bestValue = min(bestValue, result)
            beta = min(beta, bestValue)
            if beta <= alpha:
                break
        return bestValue

def minmax(game, depth):
    scored_moves = []
    for move in get_all_possible_moves(game):
        game_t = deepcopy(game)
        game_t.place(move[0], move[1])
        scored_moves.append((move, minimax_function(game_t, depth, False)))
    scored_moves.sort(key=lambda x: x[1], reverse=True)
    #print(scored_moves)
    return scored_moves[0][0] if scored_moves[0][1] != float('-inf') else None
    

def choose_piece(game):
    piece_ok = False
    while not piece_ok:
        piece_ok = game.select(random.randint(0,15))
    return True

def undo_last_move(game):
    game._board = game._last_board
    game.__selected_piece_index = game._last_choosen_piece


# Adapted
def get_all_possible_states(game_state):
    '''
    get basically all the boards
    '''
    board = game_state.get_board_status()
    return board


# get list of valid moves
def get_all_possible_moves(game_state):
    list = []
    board = game_state.get_board_status()
    #print("This is board: ", board)
    '''
    Example of board: 
    [[-1 -1 -1 -1]
    [-1 -1 -1 -1]
    [-1 -1 -1 -1]
    [-1 -1 -1 -1]]
    '''
    for i in range(4):
        for j in range(4):
            if board[i][j] == -1:
                list.append((j, i))
    return list

# new
# def get_best_move(board,depth):
#     '''
#     '''
#     bestValue=-float('inf')
#     bestMove=None 
#     chosen_piece=choose_piece(board)
#     for move in get_all_possible_moves(board,chosen_piece):
#         result=minimax(move, depth-1, False, chosen_piece, -float('inf'),float('inf'))
#         if result>bestValue:
#             bestValue=result
#             bestMove=move
#     return bestMove

def state_eval(game_state):
    '''
    Computes the evaluation of the state of the game
    '''
    if game_state.check_winner() != -1:
        return EVAL_WIN
    # is there the possibility for a tie?
    # elif game_state[0].is_full():
    # return EVAL_TIE
    else:
        return 0
