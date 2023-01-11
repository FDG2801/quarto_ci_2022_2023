# Free for personal or classroom use; see 'LICENSE.md' for details.
# https://github.com/squillero/computational-intelligence

import itertools
import logging
import argparse
import random
from .quarto.objects import Player, Quarto
from .reinforcement.rl_agent import QLAgent

class RandomPlayer(Player):
    """Random player"""

    def __init__(self, game: Quarto) -> None:
        super().__init__(game)
    #choose piece -> int 
    def choose_piece(self) -> int:
        return random.randint(0, 15)
    def place_piece(self) -> tuple[int, int]:
        return random.randint(0, 3), random.randint(0, 3)


def main():
    info = {
        'alpha': 0.3,
        'gamma': 0.9,
        'epsilon': 0.1,
        'train': True
    }

    game = Quarto()
    game.set_players((RandomPlayer(game), QLAgent(game, info)))
    winner = game.run()
    logging.warning(f"main: Winner: player {winner}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='count', default=0, help='increase log verbosity')
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