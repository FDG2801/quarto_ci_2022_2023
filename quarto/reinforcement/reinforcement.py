from collections import defaultdict
import numpy as np

class QLearningAgent:
    def __init__(self, alpha, epsilon, discount, get_legal_actions):
        self.get_legal_actions = get_legal_actions
        self._qvalues = defaultdict(lambda: defaultdict(lambda: 0))
        self.alpha = alpha
        self.epsilon = epsilon
        self.discount = discount
        
    def get_qvalue(self, state, action):
        return self._qvalues[state][action]

    def set_qvalue(self, state, action, value):
        self._qvalues[state][action] = value

    def get_value(self, state):
        possible_actions = self.possible_actions(state)

        if not possible_actions:
            return 0.0

        q_values = [self.get_qvalue(state, action) for action in possible_actions]
        return max(q_values)

    def update(self, state, action, reward, next_state):
        gamma = self.discount
        learning_rate = self.alpha
        next_max = self.get_value(next_state)
        new_q = reward + gamma * next_max
        old_q = self.get_qvalue(state, action)
        self.set_qvalue(state, action, (1 - learning_rate) * old_q + learning_rate * new_q)
