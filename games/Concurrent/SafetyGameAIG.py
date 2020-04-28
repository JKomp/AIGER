import random as rd
import AbsStochasticConcurrentGame as ac
import aigsim as ag

class SafetyGame3(ac.AbsStochasticConcurrentGame):

    def __init__(self,modelName):
        super().__init__()
        self.n_max_actions  = 2
        self.n_min_actions  = 2
        
        self.pOptions = [False] * 4
        
        print(modelName)
        
        self.model = ag.Model()

        reader = ag.Reader()
        reader.openFile(modelName)
        reader.readHeader(self.model)
        reader.readModel(self.model)

        self.model.printSelf()
        
        self.model.initModel()
        self.n_observations = pow(2,self.model.num_latches)
        
        self.tmpcnt = 0
        
    def reset(self):
        self.state = 0
        return self.state
        
    def step(self,max_action,min_action):
        
#        self.model.step('{:1d}{:1d}'.format(max_action,min_action))
        self.model.step('{:1d}{:1d}'.format(min_action,max_action))
        status = self.model.stateStr()
        
        states = status.split()
        
        self.state = int(states[2],2)
        
        result = int(states[2],2)
        if result == 1:
        	done = True
        	reward = -1
        else:
            done = False
            reward = 0
        
#         print(states, result, self.state)
#         self.tmpcnt += 1
#         if self.tmpcnt > 10:
#             print(fart)
            
        return self.state, reward, done        
 