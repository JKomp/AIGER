import random as rd
import AbsStochasticConcurrentGame as ac
import aigsim as ag

class SafetyGame2(ac.AbsStochasticConcurrentGame):

    modelName = 'aigTestSMV2.aag.txt'
    
    def __init__(self):
        super().__init__()
        self.n_observations = 4
        self.n_max_actions  = 2
        self.n_min_actions  = 2
        
        self.pOptions = [False] * 4
        
        print("SafetyGame2")
        
        self.model = ag.Model()

        reader = ag.Reader()
        reader.openFile(self.modelName)
        reader.readHeader(self.model)
        reader.readModel(self.model)

        self.model.printSelf()
        
        self.model.initModel()
        
        self.tmpcnt = 0
        
    def reset(self):
        self.state = 0
        return self.state
        
    def step(self,max_action,min_action):
        
        self.model.step('{:1d}{:1d}'.format(max_action,min_action))
        status = self.model.stateStr()
        
        states = status.split()
        
        # The next latch state defines the nest state; Map the latch values to the state diagram
        if states[3] == '11':
            self.state = 0
        elif states[3] == '01':
            self.state = 1
        elif states[3] == '00':
            self.state = 2
        elif states[3] == '10':
            self.state = 3
            
        
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
 