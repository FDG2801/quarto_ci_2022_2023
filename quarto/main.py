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
