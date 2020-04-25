import random as rd
import AbsStochasticGame as ab

class SafetyGame(ab.AbsStochasticGame):

    def __init__(self):
        self.n_states = 6
        self.n_actions = 2
        self.n_players = 2

    def init(self):
        return 0

    def step(self,curr_state,action):

        if curr_state == 0 and action == 0:
            reward = 0
            next_state = 4
        elif curr_state == 0 and action == 1:
            reward = 0
            next_state = 5

        elif curr_state == 1 and action == 0:
            reward = 0
            next_state = 4
        elif curr_state == 1 and action == 1:
            reward = 0
            next_state = 5

        elif curr_state == 2 and action == 0:
            reward = 0
            next_state = 4
        elif curr_state == 2 and action == 1:
            reward = 0
            next_state = 5

        elif curr_state == 3 and action == 0:
            reward = 0
            next_state = 4
        elif curr_state == 3 and action == 1:
            reward = 0
            next_state = 5

        elif curr_state == 4 and action == 0:
            reward = 0
            next_state = 2
        elif curr_state == 4 and action == 1:
            reward = 1
            next_state = 0

        elif curr_state == 5 and action == 0:
            reward = 0
            next_state = 2
        elif curr_state == 5 and action == 1:
            reward = -1
            next_state = 3
            
        else:
            print('invalid state {:d}'.format(curr_state))

        return next_state, reward, False

    def player(self,curr_state):

        if curr_state < 4:
            curr_player = 1
        else:
            curr_player = 0

        return curr_player
