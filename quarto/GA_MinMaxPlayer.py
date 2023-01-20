import copy
import logging
import random
from collections import namedtuple
from itertools import combinations

import numpy
from tqdm import tqdm
import numpy as np
import quarto
import MinMax_Player
import RandomPlayer


def cook_status(game, board: numpy.ndarray) -> dict:
    status = dict()

    high_values = [
        elem for elem in board.ravel() if elem >= 0 and game.get_piece_charachteristics(elem).HIGH
    ]
    coloured_values = [
        elem for elem in board.ravel() if elem >= 0 and game.get_piece_charachteristics(elem).COLOURED
    ]
    solid_values = [
        elem for elem in board.ravel() if elem >= 0 and game.get_piece_charachteristics(elem).SOLID
    ]
    square_values = [
        elem for elem in board.ravel() if elem >= 0 and game.get_piece_charachteristics(elem).SQUARE
    ]
    low_values = [
        elem for elem in board.ravel() if elem >= 0 and not game.get_piece_charachteristics(elem).HIGH
    ]
    noncolor_values = [
        elem for elem in board.ravel() if elem >= 0 and not game.get_piece_charachteristics(elem).COLOURED
    ]
    hollow_values = [
        elem for elem in board.ravel() if elem >= 0 and not game.get_piece_charachteristics(elem).SOLID
    ]
    circle_values = [
        elem for elem in board.ravel() if elem >= 0 and not game.get_piece_charachteristics(elem).SQUARE
    ]

    elements_per_type = [(len(high_values), 8), (len(coloured_values), 4), (len(solid_values), 2),
                         (len(square_values), 1),
                         (len(low_values), 0), (len(noncolor_values), 0), (len(hollow_values), 0),
                         (len(circle_values), 0)]

    rows_at_risk = list()
    columns_at_risk = list()
    diagonals_at_risk = list()
    for i in range(5):
        rows_at_risk.append(list())
        columns_at_risk.append(list())

    # 0 empty cells -> risk is 0
    # 1 empty cells -> risk is 4
    # 2 empty cells -> risk is 3
    # 3 empty cells -> risk is 2
    # 4 empty cells -> risk is 1
    for i in range(4):
        rows_at_risk[abs(list(board[i]).count(-1) - 5) % 5].append(i)
        columns_at_risk[abs(list(np.array(board).T[i]).count(-1) - 5) % 5].append(i)

    holes_count_main = 0
    holes_count_secondary = 0
    for i in range(4):
        if board[i][i] == -1:
            holes_count_main += 1
        if board[i][4 - i - 1] == -1:
            holes_count_secondary += 1

    if holes_count_main == 1:
        diagonals_at_risk.append(1)  # at this point the main diagonal is at risk
    if holes_count_secondary == 1:
        diagonals_at_risk.append(2)  # at this point the secondary diagonal is at risk

    holes = 0
    for i in range(4):
        holes += list(board[i]).count(-1)
    status["elements_per_type"] = elements_per_type
    status["rows_at_risk"] = rows_at_risk
    status["columns_at_risk"] = columns_at_risk
    status["diagonals_at_risk"] = diagonals_at_risk
    status["holes"] = holes

    return status


class GA_MinMaxPlayer(quarto.Player):
    def __init__(self, quarto: quarto.Quarto, genome=None) -> None:
        super().__init__(quarto)
        if genome is not None:
            self.genome = genome
        else:
            self.genome = dict()

    def get_game(self) -> quarto.Quarto:
        return super().get_game()

    def choose_piece(self) -> int:
        game = self.get_game()
        board = game.get_board_status()
        status = cook_status(game, board)
        elements_per_type = status["elements_per_type"]

        alpha = self.genome["alpha"]
        elements = 4

        not_winning_pieces = list()
        rows_high_risk = status["rows_at_risk"][4]
        columns_high_risk = status["columns_at_risk"][4]
        diagonals_high_risk = status["diagonals_at_risk"]
        minmax = MinMax_Player.MinMax(self.get_game())

        if len(diagonals_high_risk) != 0 or len(rows_high_risk) != 0 or len(columns_high_risk) != 0:
            not_winning_pieces = minmax.not_winning_pieces(board)
            if len(not_winning_pieces) == 1:
                return not_winning_pieces[0]

        if alpha < random.random():

            while True:
                sorted_combinations = list(
                    combinations(sorted(elements_per_type, key=lambda i: i[0])[:elements], r=4))
                random.shuffle(sorted_combinations)
                for combination in sorted_combinations:
                    piece_val = sum([val for e, val in combination])
                    if piece_val not in board:
                        if len(not_winning_pieces) == 0 or piece_val in not_winning_pieces:
                            return piece_val
                elements += 1
        else:
            while True:
                sorted_combinations = list(
                    combinations(sorted(elements_per_type, key=lambda i: i[0], reverse=True)[:elements], r=4))
                random.shuffle(sorted_combinations)
                for combination in sorted_combinations:
                    piece_val = sum([val for e, val in combination])
                    if piece_val not in board:
                        if len(not_winning_pieces) == 0 or piece_val in not_winning_pieces:
                            return piece_val
                elements += 1

    def place_piece(self) -> tuple[int, int]:
        game = self.get_game()
        board = game.get_board_status()
        status = cook_status(game, board)
        beta = self.genome["beta"]

        rows_high_risk = status["rows_at_risk"][4]
        columns_high_risk = status["columns_at_risk"][4]
        diagonals_high_risk = status["diagonals_at_risk"]
        minmax = MinMax_Player.MinMax(self.get_game())

        if len(diagonals_high_risk) != 0 or len(rows_high_risk) != 0 or len(columns_high_risk) != 0:
            can_beat_move = minmax.place_piece()
            #print(can_beat_move)
            if can_beat_move is not None:
                return can_beat_move

        if len(diagonals_high_risk) != 0:
            diagonal = random.choice(diagonals_high_risk)  # 1 or 2
            if diagonal == 1:
                for i in range(4):
                    if board[i][i] == -1:
                        return i, i
            else:
                for i in range(4):
                    if board[i][4 - i - 1] == -1:
                        return 4 - i - 1, i

        both_at_risk = len(rows_high_risk) != 0 and len(columns_high_risk) != 0

        if both_at_risk:
            if random.random() < 0.5:
                row_index = random.choice(rows_high_risk)
                row_to_complete = board[row_index]
                column_index = list(row_to_complete).index(-1)
                return column_index, row_index
            else:
                column_index = random.choice(columns_high_risk)
                column_to_complete = board.T[column_index]
                row_index = list(column_to_complete).index(-1)
                return column_index, row_index
        elif len(rows_high_risk) != 0:
            row_index = random.choice(rows_high_risk)
            row_to_complete = board[row_index]
            column_index = list(row_to_complete).index(-1)
            return column_index, row_index
        elif len(columns_high_risk) != 0:
            column_index = random.choice(columns_high_risk)
            column_to_complete = board.T[column_index]
            row_index = list(column_to_complete).index(-1)
            return column_index, row_index

        else:
            if random.random() < 0.5:
                risk_1 = status["rows_at_risk"][1] + status["rows_at_risk"][2]
                risk_2 = status["rows_at_risk"][3]
                weights = [bool(len(risk_1)) * (beta + .001), bool(len(risk_2)) * (1 - (beta + .001))]
                rows_no_risk = random.choices(
                    [risk_1, risk_2],
                    weights=weights)[0]
                row_index = random.choice(rows_no_risk)
                columns_indexes = [j for j, elem in enumerate(board[row_index]) if elem == -1]
                column_index = random.choice(columns_indexes)
                return column_index, row_index
            else:
                risk_1 = status["columns_at_risk"][1] + status["columns_at_risk"][2]
                risk_2 = status["columns_at_risk"][3]
                weights = [bool(len(risk_1)) * (beta + .001), bool(len(risk_2)) * (1 - (beta + .001))]
                columns_no_risk = random.choices(
                    [risk_1, risk_2],
                    weights=weights)[0]
                column_index = random.choice(columns_no_risk)
                rows_indexes = [j for j, elem in enumerate(board.T[column_index]) if elem == -1]
                row_index = random.choice(rows_indexes)
                return column_index, row_index

    def update_genome(self, new_genome):
        self.genome = new_genome


def evolve() -> dict:
    NUM_GENERATIONS = 100
    POPULATION_SIZE = 20
    OFFSPRING_SIZE = 5
    NO_OF_MATCHES_FITNESS = 100

    Individual = namedtuple("Individual", ["genome", "fitness"])

    # def play_n_games(player0, player1, genome0, genome1):
    #     wr = 0
    #     for _ in range(NO_OF_MATCHES_FITNESS):
    #         game = quarto.Quarto()
    #         game.set_players((player0(game, genome0), player1(game, genome1)))
    #
    #         winner = game.run()
    #         if winner == 0 or winner == -1:
    #             wr += 1
    #
    #     return wr / NO_OF_MATCHES_FITNESS
    def play_n_games(player0, player1, genome0):
        wr = 0
        for _ in range(NO_OF_MATCHES_FITNESS):
            game = quarto.Quarto()
            game.set_players((player0(game, genome0), player1(game)))

            winner = game.run()
            if winner == 0 or winner == -1:
                wr += 1

        return wr / NO_OF_MATCHES_FITNESS

    def generate_population():
        genome_parameters = ["alpha", "beta"]
        population = list()
        logging.info("Generating of the population")
        for _ in tqdm(range(POPULATION_SIZE)):
            genome = dict()
            for gene_name in genome_parameters:
                genome[gene_name] = round(random.random(), 1)
            population.append(Individual(genome, w(genome)))
        return population

    def tournament(population: list[Individual], tournament_size=3):
        return max(random.choices(population, k=tournament_size), key=lambda i: i.fitness)

    def cross_over(genome1: dict, genome2: dict):
        child = dict()
        genome1keys = sorted(genome1.keys())
        genome2keys = sorted(genome2.keys())
        split = random.randint(1, len(genome1keys) - 1)
        for g in genome1keys[:split]:
            child[g] = genome1[g]
        for g in genome2keys[split:]:
            child[g] = genome2[g]

        return child

    def cross_over2(genome1: dict, genome2: dict):
        child = dict()
        genome1keys = sorted(genome1.keys())
        genome2keys = sorted(genome2.keys())
        split = random.randint(1, len(genome1keys) - 1)
        for g in genome1keys[:split]:
            if outcome > .5:
                child[g] = min(round(genome1[g] + .3, 1), 1)
            else:
                child[g] = max(0, round(genome1[g] - .3, 1))
        for g in genome2keys[split:]:
            if outcome > .5:
                child[g] = min(round(genome2[g] + .3, 1), 1)
            else:
                child[g] = max(0, round(genome2[g] - .3, 1))

        return child

    def mutation(genome: dict):
        child = copy.deepcopy(genome)
        outcome = random.random()
        gene = random.choice(list(genome.keys()))
        if outcome > .5:
            child[gene] = min(round(genome[gene] + .1, 1), 1)
        else:
            child[gene] = max(0, round(genome[gene] - .1, 1))

        return child

    def w(genome):
        #wr = play_n_games(GA_MinMaxPlayer, GA_Player.GA_Player, genome, {'alpha': 0.1, 'beta': 0.3})
        wr = play_n_games(GA_MinMaxPlayer, RandomPlayer.RandomPlayer, genome)
        return wr

    def compute_GO_probs(no_of_gens, current_gen, best_fitness, avg_top_five_fitness) -> list[float, float, float]:
        generations_elapsed = current_gen / no_of_gens
        if generations_elapsed < 0.5:
            return [0.3, 0.5, 0.2]
        elif best_fitness - avg_top_five_fitness < 0.05:
            return [0.1, 0.45, 0.45]
        else:
            return [0.6, 0.2, 0.2]

    POPULATION = generate_population()
    best = Individual(dict(alpha=0.5, beta=0.5), 0)

    logging.info("Evolving...")
    genomes_log = dict()
    for g in tqdm(range(NUM_GENERATIONS)):
        offspring = list()
        genetic_operators_probs = \
            compute_GO_probs(NUM_GENERATIONS, g, best.fitness, sum(i.fitness for i in POPULATION[:5]) / 5)
        for i in range(OFFSPRING_SIZE):
            outcome = random.random()
            if outcome < genetic_operators_probs[0]:
                p = tournament(POPULATION)
                o = mutation(p.genome)
            elif outcome < sum(genetic_operators_probs[:2]):
                p1 = tournament(POPULATION)
                p2 = tournament(POPULATION)
                o = cross_over(p1.genome, p2.genome)
            else:
                p1 = tournament(POPULATION)
                p2 = tournament(POPULATION)
                o = cross_over2(p1.genome, p2.genome)
            f = w(o)
            offspring.append(Individual(o, f))
        POPULATION += offspring
        POPULATION = sorted(POPULATION, key=lambda i: i.fitness, reverse=True)[:POPULATION_SIZE]
        if POPULATION[0].fitness > best.fitness:
            best = copy.deepcopy(POPULATION[0])
        for i in POPULATION:
            if tuple(i.genome.items()) in genomes_log.keys():
                genomes_log[tuple(i.genome.items())] += [i.fitness]
            else:
                genomes_log[tuple(i.genome.items())] = [i.fitness]
    best_individuals = [
        (elem, round(sum(genomes_log[elem]) / len(genomes_log[elem]), 2))
        for elem in
        sorted(genomes_log, key=lambda i: -sum(genomes_log[i]) / len(genomes_log[i]))]
    logging.info(f"Best genome found is {best.genome} with fitness: {best.fitness}")
    logging.info(
        f"Best genome found (avg of fitness) is {best_individuals[0][0]} with avg fitness: {best_individuals[0][1]}")

    best_genome = dict()
    for (k, v) in best_individuals[0][0]:
        best_genome[k] = v
    return best_genome
