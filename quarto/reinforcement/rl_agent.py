from .Memory import RememberOrig
from ..quarto.objects import Player
import random
from .tables import Table
import numpy as np
class QLAgent(Player):
    def __init__(self, quarto, info):
        super().__init__(quarto)
        self.Q = RememberOrig(filename='./quarto/reinforcement/Q_data.dat')
        self.alpha = info['alpha']
        self.gamma = info['gamma']
        self.epsilon = info['epsilon']
        self.train = info['train']

    def possible_actions(self, state, piece) -> list:
        '''
        Retrieves all possible position coupled with the selected piece.
        '''
        if type(state) == 'list' or 'tuple':
            state = np.array(list(list(x) for x in state))
        #[print((x,y)) for x, row in enumerate(state) for y, value in enumerate(row) if value == -1]
        return [((x,y), piece) for x, row in enumerate(state) for y, value in enumerate(row) if value == -1 if self.placeable(state,x,y) ]
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
    def create_newstate(self, action):
        '''
        Auxiliary function to create a new temporary state.
        It helps the calculus on the update since Quarto and
        Player are not editable.
        '''
        (x, y), piece = action
        state_list = self.get_board()

        #check if action is legal
        if self.placeable(state_list, x, y):
            state_list[x][y] = piece
        return tuple(tuple(x) for x in state_list)
    def place_piece(self) -> tuple[int, int]:
        '''
        It places the piece with the best scores in the Q-tables
        '''
        state = self.get_board(type='tuple')
        piece = super().get_game().get_selected_piece()

        # last_state, last_action = self.state_history if self.state_history else (state, None)
        possible_actions = self.possible_actions(self.get_board(), piece)
        #print('possible actions: ', possible_actions)

        if not state in self.Q:
            self.Q[state] = Table()
            for action in possible_actions:
                self.Q[state][action] = 0.0

        if random.random() < self.epsilon:
        #if 2 < self.epsilon:
            action = random.choice(list(self.Q[state]))
        else:
            #print('action selection: ', self.Q[state])
            action = max(self.Q[state], key=self.Q[state].get)
        # create new board state with new action
        next_state = self.create_newstate(action)
        if self.train:
            self.update(state, action, next_state)

        return action[0][1], action[0][0]

    def get_qvalue(self, state, action):
        return self.Q[state][action]

    def set_qvalue(self, state, action, value):
        self.Q[state][action] = value

    def get_value(self, state, piece):
        possible_actions = self.possible_actions(state, piece)

        if not possible_actions:
            return 0.0
        if not state in self.Q:
            self.Q[state] = Table()
            for action in possible_actions:
                self.Q[state][action] = 0.0
        q_values = [self.get_qvalue(state, action) for action in possible_actions]
        return max(q_values)

    def update(self, state, action, next_state):
        '''
        Update Q-table according to Model-free Q-Learning
        '''
        _, piece = action
        reward = 0.0
        check_winner = super().get_game().check_winner()

        if check_winner >= 0:
            #print(f'winner: {check_winner}')
            reward = 1.0 if super().get_game().check_winner() == 1 else -1.0

        gamma = self.gamma
        learning_rate = self.alpha

        next_max = self.get_value(next_state, piece)
        new_q = reward + gamma * next_max
        old_q = self.get_qvalue(state, action)
        self.set_qvalue(state, action, (1 - learning_rate) * old_q + learning_rate * new_q)
