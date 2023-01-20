import quarto
import copy
import numpy
from minimax import minmax

class QuartoMinMax(quarto.Quarto):
    def __init__(self) -> None:
        '''
        This is an upgraded quarto class used by minmax to avoid creating multiple objects, what it does is saving the second-to-last move
        and restore the board after every move, this is done because minmax is recursive.

        So we introduce:
        _last_board
        _last_choosen_piece
        '''
        super().__init__()
        self._last_choosen_piece = 0
        self._last_board = 0
        
        
    

class MinMax(quarto.Player):
    """MinMax agent"""

    def __init__(self, quarto: quarto.Quarto) -> None:
        super().__init__(quarto)

    # def get_game(self) -> quarto.Quarto:
    #     return super().get_game()

    def choose_piece(self) -> int:
        ''' choose_piece using minmax ??? '''
        # print("Choosing piece -------------- ")
        # function to chose_piece
        # return random.randint(0, 15)
        # # ------------------------------------------------------
        # Choose the best piece to play with using a heuristic function
        quarto = self.get_game()
        best_score = -float('inf')
        best_piece = None
        for piece in range(15):
            if self.piece_available(piece):
                score = self.heuristic()
                if score > best_score:
                    best_score = score
                    best_piece = piece
        # print('best piece: ',best_piece)
        return best_piece

    def place_piece(self) -> tuple[int, int]:
        '''place_piece using minmax ??? '''
        #print("Placing piece -------------- ")
        game = self.get_game()
        game_test = QuartoMinMax()
        game_test._board = game._board
        game_test._current_player = game._current_player
        index = int(game.get_selected_piece())
        game_test.__selected_piece_index = index
        game_test._last_choosen_piece = index
        game_test._last_board = game._board
        move = minmax(game, 1)
        #print(move)
        return move  # problem here
        
        #return random.randint(0, 3), random.randint(0, 3)
        

        # Choose a position to place the piece based on a heuristic function
        # quarto = self.get_game()
        #best_score = -float('inf')
        #best_move = None
        #for move in self.possible_moves():
        #    new_board = quarto.get_board_status()
        #    score = self.heuristic()
        #    if score > best_score:
        #        best_score = score
        #        best_move = move
        #        # print("Best move: ",best_move)
        #        # piece=self.choose_piece()
        #        # self.modify_board(new_board,piece,best_move)
        #return best_move[1], best_move[0]
        # ---------------------------------------------------------

    def can_beat_one_level(self) -> tuple[bool, tuple]:
        # Choose a position to place the piece based on a heuristic function
        current_quarto = self.get_game()
        score = 0
        for move in self.possible_moves():
            quarto_copy = copy.deepcopy(current_quarto)

            quarto_copy.place(move[0], move[1])
            score = self.heuristic2(quarto_copy)
            if score == float('inf'):
                return True, (move[1], move[0])

        return False, None

    def not_winning_pieces(self, board: numpy.ndarray) -> list:
        current_quarto = self.get_game()
        available_pieces = list(set(range(16)) - set(board.ravel()))
        not_winning_pieces = list()
        moves = []
        for i in range(4):
            for j in range(4):
                if board[i][j] == -1:
                    moves.append((i, j))
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

    # def modify_board(self, board,piece,pos):
    #     print("Modifying board ------")
    #     board[pos[0]][pos[1]] = piece
    #     print("Modified board ------")
    #     print(board)

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
