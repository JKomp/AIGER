import random as rd
import AbsStochasticConcurrentGame as ac

class TemperatureGame(ac.AbsStochasticConcurrentGame):

    wx = 0.6
    wn = 0.4
    bias = 2.5
    
    def __init__(self):
        super().__init__()
        self.n_observations = 10
        self.n_max_actions  = 5
        self.n_min_actions  = 4
        print('Temperature Game')
        
    def reset(self):
        self.state = 5
        return self.state
    
    def step(self,max_action,min_action):
        
        done = False
        
#         print((self.wx * max_action + self.wn * min_action - self.bias))
        new_state = self.state + round(self.wx * max_action + self.wn * min_action - self.bias)
        
        if new_state > 10:
            self.state = 10
            done = True
            
        elif new_state < 0:
            new_state = 0
            done = True
            
        else:
            self.state = new_state
            
        reward = 4 - abs(5 - new_state)
        
        observation = int(self.state)
        
        return observation, reward, done
