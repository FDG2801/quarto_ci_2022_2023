from itertools import combinations
from reinforcement.Memory import RememberOrig
import MinMax_Player
from quarto.objects import Player
import random
from reinforcement.tables import Table
import numpy as np
import copy
from reinforcement.utils import cook_status
class QLAgent(Player):
    def __init__(self, quarto, info, genome):
        super().__init__(quarto)
        self.Q = RememberOrig(filename=info['Q_path'])
        self.alpha = info['alpha']
        self.gamma = info['gamma']
        self.epsilon = info['epsilon']
        self.train = info['train']
        self.state_history = ()
        self.quarto = quarto
        self.genome = genome

    def set_game(self, quarto):
        super().__init__(quarto)
        self.state_history = ()

    def possible_actions(self, state, piece) -> list:
        '''
        Retrieves all possible position coupled with the selected piece.
        '''
        if type(state) == ('list' or 'tuple'):
            state = np.array(list(list(x) for x in state))
        return [((x, y), piece) for x, row in enumerate(state) for y, value in enumerate(row)
                if value == -1 if self.placeable(state, x, y)]

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

    def get_board(self, type='list'):
        if type == 'tuple':
            return tuple(tuple(x) for x in super().get_game().get_board_status())
        else:
            return super().get_game().get_board_status()

    def placeable(self, state, x: int, y: int) -> bool:
        if type(state) == 'list':
            state = np.array(list(list(x) for x in state))
        return not (y < 0 or x < 0 or x > 3 or y > 3 or state[x, y] >= 0)

    def place_piece(self) -> tuple[int, int]:
        '''
        It places the piece with the best scores in the Q-tables
        '''

        if self.train:
            action = self.q_move()

            self.q_post()
            # print('======= ACTION ========')
            return action[0][1], action[0][0]
        else:
            return self.get_value()

    def q_move(self) -> tuple[int, int]:
        state = self.get_board(type='tuple')
        piece = super().get_game().get_selected_piece()
        (last_state, last_action) = self.state_history if self.state_history else (state, None)

        possible_actions = self.possible_actions(self.get_board(), piece)

        if not state in self.Q:
            self.Q[state] = Table()
            for action in possible_actions:
                self.Q[state][action] = 0.0
        elif possible_actions != list(self.Q[state]):
            for action in possible_actions:
                self.Q[state][action] = 0.0

        legal_qtable = {k: v for k, v in self.Q[state].items() if k in possible_actions}

        if random.random() < self.epsilon:
            action = random.choice(list(legal_qtable))
        else:
            # action = max(self.Q[state], key=self.Q[state].get)
            action = max(legal_qtable, key=legal_qtable.get)

        if not last_action is None:
            r = 0.0
            self.Q[last_state][last_action] += self.alpha * (
                    r + self.gamma * max([self.Q[state][a] for a in self.Q[state]]) -
                    self.Q[last_state][last_action]
            )

        self.state_history = (state, action)
        return action

    def get_value(self):
        state = self.get_board(type='tuple')
        action = max(self.Q[state], key=self.Q[state].get)
        return action[0][1], action[0][0]

    def q_post(self, winner=0.0):
        '''
        Update Q-table according to Model-free Q-Learning
        '''

        (state, action) = self.state_history
        reward = 0.0
        if winner >= 0:
            # reward = 1.0 if super().get_game().check_winner() == 1 else -1.0
            reward = 1.0 if winner == 1 else -1.0

        '''
        next_max = self.get_value(next_state, piece)
        next_max = self.Q[state][action]
        new_q = reward + gamma * next_max
        old_q = self.get_qvalue(last_state, last_action)'''
        if not action is None:
            self.Q[state][action] += self.alpha * (
                    reward - self.Q[state][action]
            )
