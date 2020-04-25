class AbsStochasticConcurrentGame():
    
    def __init__(self,observations=0,maxActions=0,minActions=0):
        self.n_observations = observations
        self.n_max_actions  = maxActions
        self.n_min_actions  = minActions
        
    def get_n_observations(self):
        return self.n_observations
    
    def get_n_max_actions(self):
        return self.n_max_actions
    
    def get_n_min_actions(self):
        return self.n_min_actions
    
    def reset(self):
        pass
    
    def step(self):
        pass
          