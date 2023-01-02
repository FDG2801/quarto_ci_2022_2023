import logging
import argparse
import random
import quarto
#from minimax import minimax_function
from GA_Player import evolve, GA_Player
from RandomPlayer import RandomPlayer


class MinMax(quarto.Player):
    """MinMax agent"""

    def __init__(self, quarto: quarto.Quarto) -> None:
        super().__init__(quarto)

    def choose_piece(self) -> int:
        ''' choose_piece using minmax ??? '''
        # function to chose_piece
        return random.randint(0, 15)

    def place_piece(self) -> tuple[int, int]:
        '''place_piece using minmax ??? '''
        #return minimax_function(self.get_game(), 5, False)  # problem here
        return random.randint(0, 3), random.randint(0, 3)

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
