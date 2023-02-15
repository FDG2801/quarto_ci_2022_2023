import quarto
import copy
import numpy
from minimax import play

class MinMax(quarto.Player):
    """MinMax agent"""

    def __init__(self, quarto: quarto.Quarto) -> None:
        super().__init__(quarto)


    def place_piece(self, depth) -> tuple[int, int]:
        '''place_piece using minmax'''
        game = self.get_game()
        move = play(game, depth)
        return move 

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

    def heuristic2(self, new_quarto: quarto.Quarto):
        if new_quarto.check_winner() >= 0:
        #if new_quarto.check_finished():
            # If the move leads to a win, return a high score
            return float('inf')
        return 0

######### UNUSED FUNCTIONS ###########

    # def possible_moves(self):
    #     # Generate a list of all empty cells on the board
    #     # print("possible_moves -------------- ")
    #     quarto = self.get_game()
    #     board = quarto.get_board_status()
    #     # print("BOARD in POSSIBLE MOVES: ",board)
    #     moves = []
    #     for i in range(4):
    #         for j in range(4):
    #             if board[i][j] == -1:
    #                 moves.append((j, i))
    #     return moves

    # def game_over(self, board):
    #     # print("Checking game status -------------- ")
    #     # Check for a win in rows
    #     for row in board:
    #         # print(row,"ROW")
    #         if self.all_same(row):
    #             return True
    #     # Check for a win in columns
    #     for i in range(4):
    #         if self.all_same([board[j][i] for j in range(4)]):
    #             return True
    #     # Check for a win in diagonals
    #     if self.all_same([board[i][i] for i in range(4)]):
    #         return True
    #     if self.all_same([board[i][3 - i] for i in range(4)]):
    #         return True
    #     # Check for a draw
    #     if not any(None in row for row in board):
    #         return True
    #     # Otherwise, the game is not over
    #     return False

    # def all_same(self, items):
    #     # print("Checking items -------------- ")
    #     # Return True if all items are the same, False otherwise
    #     return len(set(items)) == 1

    # def evaluate(self, board):
    #     # print("Evaluating -------------- ")
    #     # Calculate a score for the given board position
    #     # Higher values are better for MAX, lower values are better for MIN
    #     score = 0
    #     for row in board:
    #         score += self.evaluate_row(row)
    #     for i in range(4):
    #         score += self.evaluate_row([board[j][i] for j in range(4)])
    #     score += self.evaluate_row([board[i][i] for i in range(4)])
    #     score += self.evaluate_row([board[i][3 - i] for i in range(4)])
    #     return score

    # def evaluate_row(self, row):
    #     # print("Evaluating row -------------- ")
    #     # Calculate a score for the given row
    #     # Higher values are better for MAX, lower values are better for MIN
    #     score = 0
    #     if self.all_same(row):
    #         # Bonus points for completing a row
    #         score += 10
    #     if any(cell is None for cell in row):
    #         # Bonus points for having a piece to play in an incomplete row
    #         score += 5
    #     return score
