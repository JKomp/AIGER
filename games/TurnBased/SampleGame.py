import random as rd
import AbsStochasticGame as ab

class SampleGame(ab.AbsStochasticGame):

    def __init__(self):
        self.n_states = 4
        self.n_actions = 2
        self.n_players = 2

    def init(self):
        return 0

    def step(self,curr_state,action):

        if curr_state == 0 and action == 0:
            reward = 1
            next_state = 1
        elif curr_state == 0 and action == 1:
            reward = 3
            next_state = 2

        elif curr_state == 1 and action == 0:
            reward = 1
            next_state = 0
        elif curr_state == 1 and action == 1:
            reward = 1
            next_state = 2

        elif curr_state == 2 and action == 0:
            reward = 2
            next_state = 3
        elif curr_state == 2 and action == 1:
            reward = 3
            if rd.random() <= 0.5:
                next_state = 0
            else:
                next_state = 1

        elif curr_state == 3 and action == 0:
            reward = 5
            next_state = 2
        elif curr_state == 3 and action == 1:
            reward = 2
            next_state = 1

        return next_state, reward, False

    def player(self,curr_state):

        if curr_state == 1:
            curr_player = 0
        else:
            curr_player = 1

        return curr_player
