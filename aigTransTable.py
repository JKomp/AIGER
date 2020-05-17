from dataclasses import dataclass
import numpy as np
import math

class aigTransionTable:

    tTable = []
    bTable = []
    
    def __init__(self,numLatches,numInputs):
    
        self.tTable = np.full((pow(2,numLatches),pow(2,numInputs)),float('nan'))
        self.bTable = np.full(pow(2,numLatches),float('nan'))
    	
    def updateTransTable(self,curState, nextState, stim, bad):
        
        if np.isnan(self.tTable[curState,stim]) == True:
        	self.tTable[curState,stim] = nextState
        	
        # Flag inconsistencies where the same transition goes to a different next state
        elif self.tTable[curState,stim] != nextState:
        	self.tTable[curState,stim] = -1
        	
        if bad > 0:
            self.bTable[curState] = 1

    def printTable(self,trim=True):

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
            strOut = '0'* (inputLen - len(bin(i)[2:])) + bin(i)[2:]
            print(' {:>{width}}'.format(strOut,width=inputLen),end='')
        print('')  
        print('-----','-'*(colWidth + 1)*self.tTable.shape[1])
        
        for i in range(self.tTable.shape[0]):
            outStr = '{:3d}   '.format(i)
            visitCnt = 0
            for j in range(self.tTable.shape[1]-1,-1,-1):
                if np.isnan(self.tTable[i,j]) == True:
                    outStr += ' {:>{width}}'.format('.',width=colWidth)
                else:
                    outStr += ' {:>{width}d}'.format(int(self.tTable[i,j]),width=colWidth)
                    visitCnt += 1
                    
            if not(visitCnt == 0 and trim == True) :
                print(outStr,' {:4d}'.format(visitCnt))      
        
    # For more on DOT file format see:
    # https://www.graphviz.org/doc/info/attrs.html#k:arrowType
    # https://www.graphviz.org/doc/info/lang.html
    
    def printDotFile(self,outfile):
        
        f = open(outfile,"w")

        f.write('digraph "{}" {{\n'.format(outfile))
        
        inputLen = len(bin(self.tTable.shape[1]-1)[2:])
        for i in range(self.tTable.shape[0]):
            visitCnt = 0
            for j in range(self.tTable.shape[1]):
                if np.isnan(self.tTable[i,j]) != True:
                    visitCnt += 1
            if visitCnt > 0:
                if self.bTable[i] > 0:
                    outstr = ('{:}[shape=circle,color=red];\n'.format(i))
                else:
                    outstr = ('{:}[shape=circle,color=blue];\n'.format(i))
                f.write(outstr)

        for i in range(self.tTable.shape[0]):
            outstr = ''
            for j in range(self.tTable.shape[1]):
                if np.isnan(self.tTable[i,j]) != True:
                    lbl = '0'* (inputLen - len(bin(j)[2:])) + bin(j)[2:]
                    outstr += ('{:} -> {:} [label="{:}"];\n'.format(i, int(self.tTable[i,j]),lbl))
            if len(outstr) > 0:
                f.write(outstr)
        
        f.write('}\n')
        f.close()