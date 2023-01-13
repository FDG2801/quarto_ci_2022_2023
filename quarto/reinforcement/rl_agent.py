from .Memory import RememberOrig
from ..quarto.objects import Player
import random
from .tables import Table
import numpy as np
import copy
class QLAgent(Player):
    def __init__(self, quarto, info):
        super().__init__(quarto)
        self.Q = RememberOrig(filename=info['Q_path'])
        self.alpha = info['alpha']
        self.gamma = info['gamma']
        self.epsilon = info['epsilon']
        self.train = info['train']
        self.state_history = ()
        self.quarto = quarto

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
        return random.randint(0, 15)

    def get_board(self, type='list'):
        if type == 'tuple':
            return tuple(tuple(x) for x in super().get_game().get_board_status())
        else:
            return super().get_game().get_board_status()

    def placeable(self, state, x: int, y: int) -> bool:
        if type(state) == 'list':
            state = np.array(list(list(x) for x in state))
        return not (y < 0 or x < 0 or x > 3 or y > 3 or state[x,y] >= 0)


    def place_piece(self) -> tuple[int, int]:
        '''
        It places the piece with the best scores in the Q-tables
        '''

        if self.train:
            action = self.q_move()

            self.q_post()
            #print('======= ACTION ========')
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
            #action = max(self.Q[state], key=self.Q[state].get)
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
