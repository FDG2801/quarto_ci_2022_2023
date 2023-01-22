import quarto
import copy
import numpy
from minimax import minmax

class MinMax(quarto.Player):
    """MinMax agent"""

    def __init__(self, quarto: quarto.Quarto) -> None:
        super().__init__(quarto)

    # def get_game(self) -> quarto.Quarto:
    #     return super().get_game()

    def cp(self):
        game = self.get_game()
        #print(game.get_piece_charachteristics(3).binary)
        board = game.get_board_status()
        #print(board)
        b_board = numpy.full(
            shape=(4, 4, 4), fill_value=numpy.nan)
        #print(b_board) 
        for i,r in enumerate(board):
            for j in range(len(r)):
                b_board[i,j] = game.get_piece_charachteristics(r[j]).binary if r[j] != -1 else numpy.nan
        #print(b_board)    
    
        available_pieces = list(set(range(16)) - set(game.get_board_status().ravel()))
        available_pieces = [(game.get_piece_charachteristics(p).binary, p) for p in available_pieces] # [bool,bool,bool,bool] , idx
        #piece_prop = dict()
        
        hsum =  ((b_board == 0).sum(axis = 1).sum(axis = 0), (b_board == 1).sum(axis = 1).sum(axis = 0)) #(list of num of 0s prop, list of num of 1s prop)
        vsum= ((b_board == 0).sum(axis = 0).sum(axis = 0), (b_board == 1).sum(axis = 0).sum(axis = 0))
        dsum1 = (numpy.trace((b_board == 0), axis1=0, axis2=1), numpy.trace((b_board == 1), axis1=0, axis2=1))
        dsum2 = (numpy.trace(numpy.fliplr(b_board == 0), axis1=0, axis2=1), numpy.trace(numpy.fliplr(b_board == 1), axis1=0, axis2=1))
        #print(piece_prop)
        risk_prop = []
        for i in range(2):
            risk_prop.append(hsum[i] + vsum[i] + dsum1[i] + dsum2[i])
        min_risk = (min(risk_prop[0]),min(risk_prop[1]))
        #print(risk_prop)
        #print(min_risk)
        _p = []
        for p in available_pieces:
            risk_vect = [risk_prop[0][i] if p[0][i] == 0 else risk_prop[1][i] for i in range(len(p[0]))]
            _p.append((p[1], max(risk_vect)))
        #print(_p)
        _p.sort(key = lambda x: x[1])
        #print(_p)
        return _p[0][0] if _p[0][1] == min_risk[0] or _p[0][1] == min_risk[1] else None #_p[0:(len(available_pieces)//2)]

   

    def place_piece(self, depth) -> tuple[int, int]:
        '''place_piece using minmax'''
        game = self.get_game()
        move = minmax(game, depth)
        return move 
    
    # def can_beat_one_level(self) -> tuple[bool, tuple]:
    #     # Choose a position to place the piece based on a heuristic function
    #     current_quarto = self.get_game()
    #     score = 0
    #     for move in self.possible_moves():
    #         quarto_copy = copy.deepcopy(current_quarto)

    #         quarto_copy.place(move[0], move[1])
    #         score = self.heuristic2(quarto_copy)
    #         if score == float('inf'):
    #             return True, (move[1], move[0])

    #     return False, None

    def not_winning_pieces(self, board: numpy.ndarray) -> list:
        current_quarto = self.get_game()
        available_pieces = list(set(range(16)) - set(board.ravel()))
        not_winning_pieces = list()
        moves = []
        for i in range(4):
            for j in range(4):
                if board[i][j] == -1:
                    moves.append((j, i))
        for piece in available_pieces:
            this_piece_can_win = False
            for move in moves:
                quarto_copy: quarto.Quarto = copy.deepcopy(current_quarto)
                quarto_copy.select(piece)
                quarto_copy.place(move[0], move[1])
                score = self.heuristic2(quarto_copy)
                if score == float('inf'):
                    this_piece_can_win = True
                    break
            if not this_piece_can_win:
                not_winning_pieces.append(piece)

        return not_winning_pieces

  
    def piece_available(self, piece) -> bool:
        # Iterate over the board and check if the given piece has already been played
        # print("Is piece available? -------------- ")
        quarto = self.get_game()
        board = quarto.get_board_status()
        for row in board:
            for cell in row:
                if cell == piece:
                    return False
        return True

    def heuristic(self):
        # Calculate a score for the given board position and piece
        # Higher values are better
        # print("checking heuristic -------------- ")
        quarto = self.get_game()
        score = 0
        for move in self.possible_moves():
            new_board = quarto.get_board_status()
            # print("new_board in POSSIBLE MOVES: ",new_board)
            if self.game_over(new_board):
                # If the move leads to a win, return a high score
                return float('inf')
            score += self.evaluate(new_board)
        return score

    def heuristic2(self, new_quarto: quarto.Quarto):
        if new_quarto.check_winner() >= 0:
        #if new_quarto.check_finished():
            # If the move leads to a win, return a high score
            return float('inf')
        return 0

    def possible_moves(self):
        # Generate a list of all empty cells on the board
        # print("possible_moves -------------- ")
        quarto = self.get_game()
        board = quarto.get_board_status()
        # print("BOARD in POSSIBLE MOVES: ",board)
        moves = []
        for i in range(4):
            for j in range(4):
                if board[i][j] == -1:
                    moves.append((j, i))
        return moves

    def game_over(self, board):
        # print("Checking game status -------------- ")
        # Check for a win in rows
        for row in board:
            # print(row,"ROW")
            if self.all_same(row):
                return True
        # Check for a win in columns
        for i in range(4):
            if self.all_same([board[j][i] for j in range(4)]):
                return True
        # Check for a win in diagonals
        if self.all_same([board[i][i] for i in range(4)]):
            return True
        if self.all_same([board[i][3 - i] for i in range(4)]):
            return True
        # Check for a draw
        if not any(None in row for row in board):
            return True
        # Otherwise, the game is not over
        return False

    def all_same(self, items):
        # print("Checking items -------------- ")
        # Return True if all items are the same, False otherwise
        return len(set(items)) == 1

    def evaluate(self, board):
        # print("Evaluating -------------- ")
        # Calculate a score for the given board position
        # Higher values are better for MAX, lower values are better for MIN
        score = 0
        for row in board:
            score += self.evaluate_row(row)
        for i in range(4):
            score += self.evaluate_row([board[j][i] for j in range(4)])
        score += self.evaluate_row([board[i][i] for i in range(4)])
        score += self.evaluate_row([board[i][3 - i] for i in range(4)])
        return score

    def evaluate_row(self, row):
        # print("Evaluating row -------------- ")
        # Calculate a score for the given row
        # Higher values are better for MAX, lower values are better for MIN
        score = 0
        if self.all_same(row):
            # Bonus points for completing a row
            score += 10
        if any(cell is None for cell in row):
            # Bonus points for having a piece to play in an incomplete row
            score += 5
        return score
