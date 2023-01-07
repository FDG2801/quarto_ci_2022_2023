import logging
import argparse
import random
import quarto
from GA_Player import evolve, GA_Player
from RandomPlayer import RandomPlayer


class MinMax(quarto.Player):
    """MinMax agent"""

    def __init__(self, quarto: quarto.Quarto) -> None:
        super().__init__(quarto)

    # def get_game(self) -> quarto.Quarto:
    #     return super().get_game()

    def choose_piece(self) -> int:
        ''' choose_piece using minmax ??? '''
        print("Choosing piece -------------- ")
        # function to chose_piece
        return random.randint(0, 15) 
        # # ------------------------------------------------------
        # # Choose the best piece to play with using a heuristic function
        # quarto=self.get_game()
        # best_score = -float('inf')
        # best_piece = None
        # for piece in range(0,16):
        #     if self.piece_available(piece):
        #         board=quarto.get_board_status()
        #         score = self.heuristic(board)
        #         if score > best_score:
        #             best_score = score
        #             best_piece = piece
        # return best_piece

    def place_piece (self) -> tuple[int, int]:
        '''place_piece using minmax ??? '''
        print("Placing piece -------------- ")
        #return minimax_function(self.get_game(), 5, False)  # problem here
        return random.randint(0, 3), random.randint(0, 3)
        # # -------------------------------------------------------------------
        #     # Choose a position to place the piece based on a heuristic function
        # quarto=self.get_game()
        # best_score = -float('inf')
        # best_move = None
        # for move in self.possible_moves():
        #     new_board = quarto.get_board_status()
        #     score = self.heuristic(new_board)
        #     if score > best_score:
        #         best_score = score
        #         best_move = move
        # return best_move


    # def piece_available(self, piece) -> bool:
    #     # Iterate over the board and check if the given piece has already been played
    #     print("Is piece available? -------------- ")
    #     quarto=self.get_game()
    #     board=quarto.get_board_status()
    #     for row in board:
    #         for cell in row:
    #             if cell==piece:
    #                 return False
    #     return True

    # def heuristic(self,board):
    # # Calculate a score for the given board position and piece
    # # Higher values are better
    #     print("checking heuristic -------------- ")
    #     quarto=self.get_game()
    #     score = 0
    #     for move in self.possible_moves():
    #         new_board = quarto.get_board_status()
    #         if self.game_over(new_board):
    #             # If the move leads to a win, return a high score
    #             return float('inf')
    #         score += self.evaluate(new_board)
    #     return score

    # def possible_moves(self):
    # # Generate a list of all empty cells on the board
    #     print("possible_moves -------------- ")
    #     quarto=self.get_game()
    #     board=quarto.get_board_status()
    #     moves = []
    #     for i in range(4):
    #         for j in range(4):
    #             if board[i][j] == -1:
    #                 moves.append((i, j))
    #     return moves

    # def game_over(self,board):
    #     print("Checking game status -------------- ")
    #     # Check for a win in rows
    #     for row in board:
    #         #print(row,"ROW")
    #         if self.all_same(row):
    #             return True
    #     # Check for a win in columns
    #     for i in range(4):
    #         if self.all_same([board[j][i] for j in range(4)]):
    #             return True
    #     # Check for a win in diagonals
    #     if self.all_same([board[i][i] for i in range(4)]):
    #         return True
    #     if self.all_same([board[i][3-i] for i in range(4)]):
    #         return True
    #     # Check for a draw
    #     if not any(None in row for row in board):
    #         return True
    #     # Otherwise, the game is not over
    #     return False

    # def all_same(self,items):
    #     print("Checking items -------------- ")
    #     # Return True if all items are the same, False otherwise
    #     return len(set(items)) == 1

    # def evaluate(self,board):
    #     print("Evaluating -------------- ")
    #     # Calculate a score for the given board position
    #     # Higher values are better for MAX, lower values are better for MIN
    #     score = 0
    #     for row in board:
    #         score += self.evaluate_row(row)
    #     for i in range(4):
    #         score += self.evaluate_row([board[j][i] for j in range(4)])
    #     score += self.evaluate_row([board[i][i] for i in range(4)])
    #     score += self.evaluate_row([board[i][3-i] for i in range(4)])
    #     return score

    # def evaluate_row(self,row):
    #         print("Evaluating row -------------- ")
    #         # Calculate a score for the given row
    #         # Higher values are better for MAX, lower values are better for MIN
    #         score = 0
    #         if self.all_same(row):
    #             # Bonus points for completing a row
    #             score += 10
    #         if any(cell is None for cell in row):
    #             # Bonus points for having a piece to play in an incomplete row
    #             score += 5
    #         return score

'''
def choose_piece(self) -> int:
    """Uses the minmax algorithm to choose a piece to give to the opponent."""
    best_value = float('-inf')
    best_piece = None
    for piece in self.quarto.pieces:
        value = 0
        for move in self.quarto.get_valid_moves():
            x, y = move
            game = copy.deepcopy(self.quarto)
            game.make_move(x, y, piece)
        value += game.minmax(3, float('-inf'), float('inf'), False)
        if value > best_value:
            best_value = value
            best_piece = piece
    return best_piece

def place_piece(self) -> Tuple[int, int]:
    """Uses the minmax algorithm to choose a move to make on the board."""
    best_value = float('-inf')
    best_move = None
    for move in self.quarto.get_valid_moves():
        x, y = move
        game = copy.deepcopy(self.quarto)
        game.make_move(x, y, self.quarto.chosen_piece)
        value = game.minmax(3, float('-inf'), float('inf'), True)
        if value > best_value:
        best_value = value
        best_move = move
    return best_move

def make_move(self, x: int, y: int, piece: int) -> None:
    """Makes the move (x, y) on the board with the given piece."""
    self.board[x][j] = piece
    self.pieces.remove(piece)
    self.current_player *= -1

This function sets the value of the position (x, y) on the board to the given piece, 
removes the piece from the list of remaining pieces, and flips the current player (since it is now the other player's turn).
'''


def main():
    # print("GA-----------------------------")
    # game = quarto.Quarto()
    # find_genome = evolve()

    # game.set_players((RandomPlayer(game), GA_Player(game, find_genome)))
    # winner = game.run()
    # logging.info(f"main: Winner: player {winner}")

    print("MINMAX-----------------------------")
    game = quarto.Quarto()
    
    game.set_players((RandomPlayer(game), MinMax(game)))
    winner = game.run()
    logging.info(f"main: Winner: player {winner}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='count', default=2, help='increase log verbosity')
    parser.add_argument('-d',
                        '--debug',
                        action='store_const',
                        dest='verbose',
                        const=2,
                        help='log debug messages (same as -vv)')
    args = parser.parse_args()

    if args.verbose == 0:
        logging.getLogger().setLevel(level=logging.WARNING)
    elif args.verbose == 1:
        logging.getLogger().setLevel(level=logging.INFO)
    elif args.verbose == 2:
        logging.getLogger().setLevel(level=logging.DEBUG)

    main()
