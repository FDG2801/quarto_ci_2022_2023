EVAL_TIE = 0  #  this draw value only matters in the endgame, where the heuristic doesn't matter anymore
EVAL_WIN = 9

MAX_DEPTH = 4

'''
TODO:
- game_state must be adapted with the professor's code
- test
- add heuristics (?)
'''

def minimax(game_state,depth:int,max_player:bool, alpha=float('-inf'),beta=float('inf')):
    '''
    game=self.get_game() -> Quarto type 
    board=game.get_board_status() -> ndarray
    game_state -- a tuple of three elements :
        - [0] the game_board
        - [1] the storage_board, a Board object that holds the pieces available to pick --- ???
        - [2] the selected_piece coordinates, a tuple of (x, y) coordinates that correspond to an available piece
        on the storage_board. This is the piece that has to be put on the game_board.
    depth -- int that represents the maximum depth we will explore
    max_player -- the player trying to maximize its evaluation, True if maximizing, False if minimizing
    alpha -- initialized to the worst possible evaluation, has to be None if we don't want any pruning
    beta -- initialized to the best possible evaluation, has to be None if we don't want any pruning
    Returns
    a tuple that contains :
    [0] the evaluation of the child (between -9 for a loss, and 9 for a win)
    [1] the new game_state
    '''
    game=game_state.get_game()
    board=game_state.get_board_status() #ndarray
    #Terminal state or max depth reached
    if depth==0 or game.check_winner():
        return state_eval(game_state)*(-1 if max_player else 1) # return the evaluation of the child and the child itself
    best_move=None #there are no more moves

    if max_player:
        max_eval=float('-inf')
        for child in get_all_possible_states(game_state): #get all the free positions
            evaluation=minimax(child, depth-1, False, alpha,beta)[0] #the evaluation child is at index 0
            max_eval=max(max_eval,evaluation)

            if max_eval==evaluation:
                best_move=child 
            
            #alpha-beta pruning
            if alpha and beta:
                alpha=max(alpha,max_eval)
                if beta<=alpha: #better options available
                    break
        return max_eval,best_move

    #minimize the evaluation
    else:
        min_eval=float('-inf')
        for child in get_all_possible_states(game_state): #get all the free positions
            evaluation=minimax(child, depth-1, True, alpha,beta)[0] #the evaluation child is at index 0
            max_eval=min(min_eval,evaluation)

            if max_eval==evaluation:
                best_move=child 
            
            #alpha-beta pruning
            if alpha and beta:
                beta=min(beta,min_eval)
                if beta<=alpha: #better options available
                    break
        return min_eval,best_move 

def get_all_possible_states(game_state):
    '''
    get basically all the boards
    '''
    board=game_state.get_status_board()
    return board

def get_all_possible_moves(game_state):
    list=[]
    board=game_state.get_status_board()
    for i in board:
        for j in board[0]:
            if board[i][j]==-1:
                list.append([i,j])
    return list

def state_eval(game_state):
    '''
    Computes the evaluation of the state of the game
    '''
    game=game_state.get_game()
    if game.check_winner():
        return EVAL_WIN
    #is there the possibility? 
    #elif game_state[0].is_full():
        #return EVAL_TIE
    else:
        return 0 
