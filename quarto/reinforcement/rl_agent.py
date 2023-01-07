from .Memory import RememberOrig
from ..quarto.objects import Player
from random import random

class QLAgent(Player):
    def __init__(self, quarto, info):
        super().__init__(quarto)
        self.Q = RememberOrig(filename='./quarto/reinforcement/Q_data.dat')
        self.alpha = info['alpha']
        self.gamma = info['gamma']
        self.epsilon = info['epsilon']
        self.state_history = []

    def possible_actions(state) -> list:
        return [index for index, value in enumerate(state.get_board_status()) if value == -1]

    def choose_piece(self) -> int:
        '''
        at the moment it uses the same strategy as random to retrieve
        a piece to be placed by the counterpart.
        To be implemented better.
        '''
        return random.randint(0, 15)

    def place_piece(self) -> tuple[int, int]:
        '''
        It places the piece with the best scores in the Q-tables
        '''


        return

    def get_qvalue(self, state, action):
        return self.Q[state][action]

    def set_qvalue(self, state, action, value):
        self.Q[state][action] = value

    def get_value(self, state):
        possible_actions = self.possible_actions(state)

        if not possible_actions:
            return 0.0
        if random.random() < self.epsilon:
            action = random.choice(list(self.Q[state.get_board_status]))
        q_values = [self.get_qvalue(state, action) for action in possible_actions]
        return max(q_values)

    def update(self, state, action, reward, next_state):
        '''
        Update Q-table according to Model-free Q-Learning
        '''
        gamma = self.discount
        learning_rate = self.alpha
        next_max = self.get_value(next_state)
        new_q = reward + gamma * next_max
        old_q = self.get_qvalue(state, action)
        self.set_qvalue(state, action, (1 - learning_rate) * old_q + learning_rate * new_q)
