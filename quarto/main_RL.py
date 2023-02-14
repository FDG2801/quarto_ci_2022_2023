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
import numpy as np
from RandomPlayer import RandomPlayer

def train_test(info, genome, train_iterations: int, precision: int, versus: str):
    '''
        Modify info['train'] to choose training or testing modality
    '''

    max_wr = (0, -1)
    move_history = []
    indices = []
    path = info['Q_path']
    won = 0
    draw = 0
    game = Quarto()
    agent = QLAgent(game, info, genome)
    if versus == 'GA':
        game.set_players((GA_Player(game, {'alpha': 0.1, 'beta': 0.3}), agent))
    elif versus == 'Random':
        game.set_players((RandomPlayer(game), agent))

    for m in tqdm(range(train_iterations)):
        winner = game.run()
        if info['train']:
            agent.q_post(winner=winner)

        if winner == 1:
            won += 1
        elif winner == -1:
            draw += 1

        if m % precision == 0 and m > 0:
            winrate = won / precision * 100

            logging.debug(f"{m}: won: {winrate} | draw : {draw / precision * 100}")

            move_history.append(winrate)
            indices.append(m)
            won = 0
            draw = 0
            if max_wr[0] < winrate:
                max_wr = (winrate, m)
        game.reset()

    avg_wr = np.array(move_history).mean()
    logging.info(f'max winrate: {max_wr} | avg winrate: {avg_wr}')
    plt.ylabel('winrate %')
    plt.xlabel('# games')
    plt.ylim(0, 100)
    plt.plot(indices, move_history, "b")
    plt.show()

    if not info['train']:
        plt.savefig(f'./RL&GA_vs_{versus}_2nd_test.svg')
    else:
        plt.savefig(f'./RL&GA_vs_{versus}_2nd_train.svg')
        Save(agent.Q, path)

def main():
    info = {
        'alpha': 0.1,   # learning rate
        'gamma': 0.9,   # memory
        'epsilon': 1,   # chance of making a random move
        'min_epsilon': 0.1,
        'epsilon_decay': 0.9995,
        'train': True,  # Choose
        'Q_path': './quarto/reinforcement/Q_data_RL_GA.dat'
    }
    
    genome = {'alpha': 0.1, 'beta': 0.3}
    # Train against GA
    train_test(info, genome, 100_000, 1_000, 'GA')

    info['train'] = False
    # Test against GA, trained against GA
    train_test(info, genome, 100_000, 1_000, 'GA')
    # Test against Random, trained against GA
    train_test(info, genome, 100_000, 1_000, 'Random')


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