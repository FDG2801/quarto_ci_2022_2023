from .Memory import RememberOrig
from ..quarto.objects import Player
import random
from .tables import Table
import numpy as np
import copy
import logging
class QLAgent(Player):
    def __init__(self, quarto, info):
        super().__init__(quarto)
        self.Q = RememberOrig(filename=info['Q_path'])
        self.alpha = info['alpha']
        self.gamma = info['gamma']
        self.epsilon = info['epsilon']
        self.min_epsilon = info['min_epsilon']
        self.epsilon_decay = info['epsilon_decay']
        self.train = info['train']
        self.state_history = None
        self.quarto = quarto
        self.available_pieces = {i for i in range(16)}

        self.games = 0

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
        '''
        at the moment it uses the same strategy as random to retrieve
        a piece to be placed by the counterpart.
        To be implemented better.

        Possible idea is to retrieve the piece which minimizes the Q-table score,
        or to create a new Q-table.
        '''
        state = self.get_board(type='tuple')
        piece = None
        available_pieces = self.get_available_pieces()

        # Check if state is in Q_table with 3 rotations
        for i in [1,2,3]:
            state_tmp = self.get_board(type='tuple', X=np.rot90(self.get_board(), i))
            if state_tmp in self.Q:
                state = state_tmp
                break

        if state in self.Q and self.games > 50_000:
            legal_pieces = {k: v for k, v in self.Q[state].items() if k[1] in available_pieces}
            _, piece = min(legal_pieces, key=legal_pieces.get)
            logging.debug(f'RL gives other {piece=}')
        else:
            piece = random.randint(0, 15)

        return piece

    def get_available_pieces(self) -> list:
        state = super().get_game().get_board_status()
        placed = {value for x, row in enumerate(state) for y, value in enumerate(row) if value != -1}

        return list(self.available_pieces.difference(placed))

    def get_board(self, type='list', X = None):
        if X is None:
            X = super().get_game().get_board_status()
        if type == 'tuple':
            return tuple(tuple(x) for x in X)
        else:
            return X

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

            #self.q_post()
            #print('======= ACTION ========')
            return action[0][1], action[0][0]
        else:
            return self.get_value()

    def q_move(self) -> tuple[int, int]:
        state = self.get_board(type='tuple')
        state_np = self.get_board()
        piece = super().get_game().get_selected_piece()
        (last_state, last_action) = self.state_history if self.state_history else (state, None)

        possible_actions = self.possible_actions(self.get_board(), piece)

        # Check if state is in Q_table with 3 rotations
        for i in [1,2,3]:
            state_tmp = self.get_board(type='tuple', X=np.rot90(state_np, i))
            if state_tmp in self.Q:
                state = state_tmp
                break

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
            #action = max(self.Q[state], key=self.Q[state].get)
            action = max(legal_qtable, key=legal_qtable.get)
        future_state = self.create_state(action)

        if not last_action is None:
            r = 0.0
            self.Q[state][action] += self.alpha * (
                r + self.gamma * self.get_qvalue(future_state) -
                self.Q[state][action]
            )

        self.state_history = (state, action)
        return action

    def create_state(self, action) -> tuple:
        state_np = self.get_board()
        state_np[action[0][0], action[0][1]] = action[1]
        return self.get_board(type='tuple', X=state_np)

    def get_qvalue(self, state):

        if state not in self.Q or self.Q[state] is None:
            return 0.0
        return max(self.Q[state].values())

    def get_value(self):
        state = self.get_board(type='tuple')
        action = max(self.Q[state], key=self.Q[state].get)
        return action[0][1], action[0][0]

    def q_post(self, winner=None):
        '''
        Update Q-table according to Model-free Q-Learning
        '''

        (state, action) = self.state_history
        reward = 0.0
        if winner is not None:
            if winner >= 0:
                # reward = 1.0 if super().get_game().check_winner() == 1 else -1.0
                reward = 100.0 if winner == 1 else -100.0
            if winner == -1:
                reward = 0.0
            self.state_history = None

        if not action is None:
            self.Q[state][action] += self.alpha * reward

        # Update epsilon
        self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)
        self.games += 1