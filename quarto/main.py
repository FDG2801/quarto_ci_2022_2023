import logging
import argparse
import quarto
from GA_Player import evolve, GA_Player
from RandomPlayer import RandomPlayer
from MinMax_Player import MinMax


def main():
    # print("GA-----------------------------")
    # game = quarto.Quarto()
    # # find_genome = evolve()
    # found_genome = {'alpha': 0.1, 'beta': 0.3}
    # game.set_players((RandomPlayer(game), GA_Player(game, found_genome)))
    # winner = game.run()
    # logging.info(f"main: Winner: player {winner}")
    #
    # print("MINMAX-----------------------------")
    # game = quarto.Quarto()
    #
    # game.set_players((RandomPlayer(game), MinMax(game)))
    # winner = game.run()
    # logging.info(f"main: Winner: player {winner}")

    wr = 0
    print("Random vs GA")
    for _ in range(1000):
        game = quarto.Quarto()
        # find_genome = evolve()
        found_genome = {'alpha': 0.1, 'beta': 0.3}
        game.set_players((RandomPlayer(game), GA_Player(game, found_genome)))
        winner = game.run()
        if winner == 0:
            wr += 1
    print(f"wr: {wr}/1000")

    wr = 0
    print("GA vs MinMax")
    for _ in range(1000):
        game = quarto.Quarto()
        # find_genome = evolve()
        found_genome = {'alpha': 0.1, 'beta': 0.3}
        game.set_players((GA_Player(game, found_genome), MinMax(game)))
        winner = game.run()
        if winner == 0:
            wr += 1
    print(f"wr: {wr}/1000")


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
