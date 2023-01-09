from collections import namedtuple
from copy import deepcopy
import numpy as np
import random
from .tables import Table
from nim_utils import cook_status_t1
from .Memory import RememberOrig



class Q_agent:
    def __init__(self, state, info) -> None:
        self.Q = RememberOrig(filename='Q_data.dat')
        self.alpha = info['alpha']
        self.gamma = info['gamma']
        self.epsilon = info['epsilon']
        self.state_history = []

    def Q_move(self, state):
        last_state, last_action = self.state_history[-1] if self.state_history else (state.rows, None)
        #print('Move | last_state, last_action: ', (last_state, last_action))
        allowedMoves = cook_status_t1(state)["possible_moves"]
        #print('allowed: ', allowedMoves)
        #print('state.rows ', state.rows)
        if not state.rows in self.Q:
            self.Q[state.rows] = Table()
            for action in allowedMoves:
                self.Q[state.rows][action] = 0.0

        if random.random() < self.epsilon:
            action = random.choice(list(self.Q[state.rows]))
            #print('random action: ', action)
        else:
            action = max(self.Q[state.rows], key=self.Q[state.rows].get)
            #print('action: ', action)
        
        if not last_action is None:
            r = 0.0
            #print('last: ', self.Q[last_state][last_action])
            self.Q[last_state][last_action] += self.alpha * (
                r + self.gamma * max([self.Q[state.rows][a] for a in self.Q[state.rows]]) - 
                self.Q[last_state][last_action]
            )
        self.update_state_history(state, action)
        return action
    
    def update_state_history(self, state, action):
        self.state_history.append((state.rows, action))

    def Q_post(self,state,status=None):
        #last_state, last_action = self.state_history[-1]
        last_state, last_action = self.state_history[-1] if self.state_history else (state.rows, None)
        #print('Post | last_state, last_action: ', (last_state, last_action))
        if status == 'lose':
            r = -1.0
        elif status == 'win':
            r = 1.0
        else:
            r=0.0

        if not last_action is None:
            self.Q[last_state][last_action] += self.alpha * (
                r - self.Q[last_state][last_action]
            )