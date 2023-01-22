# Free for personal or classroom use; see 'LICENSE.md' for details.
# https://github.com/squillero/computational-intelligence

import itertools
import logging
import argparse
import random

from GA_Player import GA_Player
from quarto.objects import Player, Quarto
from reinforcement.rl_agent import QLAgent
from reinforcement.Memory import Save
import matplotlib.pyplot as plt
from tqdm import tqdm

class RandomPlayer(Player):
    """Random player"""

    def __init__(self, game: Quarto) -> None:
        super().__init__(game)
    #choose piece -> int
    def choose_piece(self) -> int:
        return random.randint(0, 15)
    def place_piece(self) -> tuple[int, int]:
        return random.randint(0, 3), random.randint(0, 3)

def train(info, genome, train_iterations: int):
    max_wr = (0, -1)
    move_history = []
    indices = []
    draw_hist = []
    path = info['Q_path']
    won = 0
    draw = 0
    game = Quarto()
    agent = QLAgent(game, info, genome)
    game.set_players((GA_Player(game, {'alpha': 0.1, 'beta': 0.3}), agent))

    for m in tqdm(range(train_iterations)):
        winner = game.run()
        agent.q_post(winner=winner)

        if winner == 1:
            won += 1
        elif winner == -1:
            draw += 1
    for m in tqdm(range(train_iterations)):
        winner = game.run()
        agent.q_post(winner=winner)

        if winner == 1:
            won += 1
        elif winner == -1:
            draw += 1

        if m % 10_000 == 0 and m > 0:
            winrate = won
            logging.info(f"{m}: won: {won/100} | draw : {draw/100}")
            move_history.append(winrate)
            draw_hist.append(draw)
            indices.append(m)
            won = 0
            draw = 0
            if max_wr[0] < winrate:
                max_wr = (winrate, m)
        game.reset()
        '''if m % 2 == 1:
            game.set_players((agent, GA_Player(game, {'alpha': 0.1, 'beta': 0.3})))
        else:
            game.set_players((GA_Player(game, {'alpha': 0.1, 'beta': 0.3}), agent))'''

    logging.info(f'max winrate: {max_wr}')
    plt.ylabel('winrate %')
    plt.xlabel('# games')
    plt.xlim(0, train_iterations)
    plt.ylim(0, 100)
    plt.plot(indices, move_history, "b")
    #plt.plot(indices, draw_hist, "b")
    plt.savefig('./million_RL&GA_vs_GA_2nd.svg')
    plt.show()
    Save(agent.Q, path)


def main():
    info = {
        'alpha': 0.1,   # learning rate
        'gamma': 0.9,   # memory
        'epsilon': 1,   # chance of making a random move
        'min_epsilon': 0.1,
        'epsilon_decay': 0.9995,
        'train': True,
        'Q_path': './quarto/reinforcement/Q_data.dat'
    }

    genome = {'alpha': 0.1, 'beta': 0.3}
    train(info, genome, 1_000_000)
    '''
    game = Quarto()
    agent = QLAgent(game, info)
    game.set_players((RandomPlayer(game), agent))
    winner = game.run()
    '''
    #logging.warning(f"main: Winner: player {winner}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='count', default=1, help='increase log verbosity')
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