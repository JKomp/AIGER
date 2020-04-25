import random as rd
import AbsStochasticConcurrentGame as ac
        
class SafetyGame1(ac.AbsStochasticConcurrentGame):

    def __init__(self):
        super().__init__()
        self.n_observations = 3
        self.n_max_actions  = 2
        self.n_min_actions  = 2
        print("SampleGame")
        
    def reset(self):
        self.state = 0
        return self.state
        
    def step(self,max_action,min_action):
        
        if (self.state == 0) and (max_action == 0) and (min_action == 0):
            reward = 2
            self.state = 0
        elif (self.state == 0) and (max_action == 0) and (min_action == 1):
            reward = 2
            self.state = 1
        elif (self.state == 0) and (max_action == 1):
            reward = 3
            self.state = 1
        elif (self.state == 1) and (max_action == 0):
            reward = 2
            self.state = 2
        elif (self.state == 1) and (max_action == 1):
            if rd.random() < 0.5:
                if (min_action == 0):
                    self.state = 0
                else:
                    self.state = 1
                reward = 4
            else:
                self.state = 0
                reward = 3
        elif (self.state == 2) and (max_action == 0):
            reward = 5
            self.state = 1
        elif (self.state == 2) and (max_action == 1) and (min_action == 0):
            reward = 3
            self.state = 0
        elif (self.state == 2) and (max_action == 1) and (min_action == 1):
            reward = 3
            self.state = 1
                
        done = False
        
        return self.state, reward, done        
 