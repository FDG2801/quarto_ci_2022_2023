# Free for personal or classroom use; see 'LICENSE.md' for details.
# https://github.com/squillero/computational-intelligence

import itertools
import logging
import argparse
import random
from .quarto.objects import Player, Quarto
from .reinforcement.rl_agent import QLAgent
from .reinforcement.Memory import Save
import matplotlib.pyplot as plt
class RandomPlayer(Player):
    """Random player"""

    def __init__(self, game: Quarto) -> None:
        super().__init__(game)
    #choose piece -> int
    def choose_piece(self) -> int:
        return random.randint(0, 15)
    def place_piece(self) -> tuple[int, int]:
        return random.randint(0, 3), random.randint(0, 3)

def train(info, train_iterations: int):
    max_wr = (0, -1)
    move_history = []
    indices = []
    won = 0
    game = Quarto()
    path = info['Q_path']

    agent = QLAgent(game, info)
    game.set_players((RandomPlayer(game), agent))

    for m in range(train_iterations):
        winner = game.run()
        agent.q_post(winner=winner)

        if winner == 1:
            won += 1
        if m % 100 == 0 and m > 0:
            print(f"{m}: {won}")
            winrate = won
            move_history.append(winrate)
            indices.append(m)
            won = 0
            if max_wr[0] < winrate:
                max_wr = (winrate, m)
        game = Quarto()
        agent.set_game(game)
        game.set_players((RandomPlayer(game), agent))

    Save(agent.Q, path)
    logging.warning(f'max winrate: {max_wr}')
    plt.ylabel('winrate %')
    plt.xlabel('# games')
    plt.ylim(0, 100)
    plt.plot(indices, move_history, "b")
    plt.show()
def main():
    info = {
        'alpha': 0.3,   # learning rate
        'gamma': 0.9,   # memory
        'epsilon': 0.2, # chance of making a random move
        'train': True,
        'Q_path': './quarto/reinforcement/Q_data.dat'
    }



    train(info, 10000)
    #
    '''
    game = Quarto()
    agent = QLAgent(game, info)
    game.set_players((RandomPlayer(game), agent))
    winner = game.run()
    '''
    #logging.warning(f"main: Winner: player {winner}")

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