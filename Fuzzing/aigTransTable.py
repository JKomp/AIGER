from dataclasses import dataclass
import numpy as np
import math

class aigTransionTable:

    tTable = []
    
    def __init__(self,numLatches,numInputs):
    
        self.tTable = np.full((pow(2,numLatches),pow(2,numInputs)),float('nan'))
        pass
    	
    def updateTransTable(self,curState, nextState, stim):
        
        self.tTable[curState,stim] = nextState

    def printTable(self):

        inputLen = len(bin(self.tTable.shape[1]-1)[2:])
        stateLen = len(str(self.tTable.shape[0]))
        
        if stateLen > inputLen:
            colWidth = stateLen
        else:
            colWidth = inputLen
            
        print('\nTransistion Table')   
        print('------------------')    
        print('\n        Input')
        print('     ','-'*(colWidth + 1)*self.tTable.shape[1])
         
        print('State ',end='')
        for i in range(self.tTable.shape[1]-1,-1,-1):
            strOut = bin(i)[2:]
            strOut = '0'* (inputLen - len(bin(i)[2:])) + strOut
            print(' {:>{width}}'.format(strOut,width=inputLen),end='')
        print('')  
        print('-----','-'*(colWidth + 1)*self.tTable.shape[1])
        
        for i in range(self.tTable.shape[0]):
            print('{:3d}   '.format(i),end='')
            for j in range(self.tTable.shape[1]-1,-1,-1):
                if np.isnan(self.tTable[i][j]) == True:
                    print(' {:>{width}}'.format('.',width=colWidth),end='')
                else:
                    print(' {:>{width}d}'.format(int(self.tTable[i][j]),width=colWidth),end='')
            print('')      
        