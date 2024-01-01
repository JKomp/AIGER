import sys
import os
import argparse

from dataclasses import dataclass

import aigsimgates as ag
import aigTransTable as tt

# Implementation of a very stripped down version of the C program aigsim

# Source Files
# modelFile = 'aigTestSMV2.aag.txt'
# stimFile  = 'stim1.txt'
modelFile = 'aigTestLatch.aag.txt'
stimFile  = 'stimELatchSmall.txt'

STORE_PATH = '/Users/john/Jupyter/Machine Learning'

validInput = {"0","1"}

from dataclasses import dataclass
        
@dataclass
class Reader:
    
    inFile = ''
    
    def _init_(self):
        pass

#--------------------------------------------------------------------------------------
    
    def openFile(self,file):
        
        self.inFile = open(file)

#--------------------------------------------------------------------------------------

    def procModelNames(self,model):
    
        for line in self.inFile:
            gateNames = line.split(' ',1)
            if gateNames[0][0] != 'c':
                if gateNames[0][0] == 'i':
                    model.inputs[int(gateNames[0][1:])].setModName(gateNames[1].rstrip())
                    
                elif gateNames[0][0] == 'l':
                    model.latches[int(gateNames[0][1:])].setModName(gateNames[1].rstrip())
                
                elif gateNames[0][0] == 'o':
                    model.outputs[int(gateNames[0][1:])].setModName(gateNames[1].rstrip())

            else:
                break

        
#--------------------------------------------------------------------------------------
        
    def readHeader(self,model):
        
        args = (self.inFile.readline()).split()
        
        if args[0] != 'aag':
            return -1
        
        if len(args) < 6:
            sys.exit('Insufficient model parameters MILOA minimum requirement')
            
        model.maxvar      = int(args[1])
        model.num_inputs  = int(args[2])
        model.num_latches = int(args[3])
        model.num_outputs = int(args[4])
        model.num_ands    = int(args[5])
        
        if len(args) >= 7:
            model.num_bad = int(args[6])
            
        if len(args) >= 8:
            model.num_constraints = int(args[7])
       
        if len(args) >= 9:
            model.num_justice = int(args[8])

        if len(args) >= 10:
            model.num_fairness = int(args[9])

        return 0

#--------------------------------------------------------------------------------------
    
    def validateInput(self,numArgs,errStr,verbose):
        
        args = (self.inFile.readline()).split()
        
        err = 0
        if len(args) < numArgs:
            print(errStr)
            err = -1
        
        if verbose == True:
            print(args)
            
        return args,err

#--------------------------------------------------------------------------------------

    def readModel(self,model):
        
        verbose = False
        gateList = [0] * (model.maxvar + 1)
        gateList[0] = ag.aiger_const(0,'Constant',0)
        
        model.inputs = [0]*model.num_inputs
        for i in range(0,model.num_inputs):
            args,err = self.validateInput(1,'Invalid model definition - Input',verbose)
            if err == 0:
                model.inputs[i] = ag.aiger_input(int(args[0]),'Input',i)
                gateList[int(int(args[0])/2)] = model.inputs[i]
                 
        model.latches = [0]*model.num_latches
        for i in range(0,model.num_latches):
            args,err = self.validateInput(2,'Invalid model definition - Latches',verbose)
            if err == 0:
                if len(args) == 2:
                    args.append('0')
                model.latches[i] = ag.aiger_latch(int(args[0]),int(args[1]),int(args[2]),i)
                gateList[int(int(args[0])/2)] = model.latches[i]
        
        model.outputs = [0]*model.num_outputs
        for i in range(0,model.num_outputs):
            args,err = self.validateInput(1,'Invalid model definition - Output',verbose)
            if err == 0:
                model.outputs[i] = ag.aiger_output(int(args[0]),'Output',i)
        
        model.bad = [0]*model.num_bad
        for i in range(0,model.num_bad):
            args,err = self.validateInput(1,'Invalid model definition - Bad State',verbose)
            if err == 0:
                model.bad[i] = ag.aiger_output(int(args[0]),'Bad',i)
            
        model.constraint = [0]*model.num_constraints
        for i in range(0,model.num_constraints):
            args,err = self.validateInput(1,'Invalid model definition - Constraints',verbose)
            if err == 0:
                model.constraint[i] = ag.aiger_output(int(args[0]),'Const',i)

        # Read but ignore any justice properties 
        if model.num_justice > 0:
            justiceSizes = [0]*model.num_justice
            for j in range(0,model.num_justice):
                justiceSizes[j] = int((self.inFile.readline()).split()[0])

            for j in range(0,model.num_justice):
                for k in range(0,justiceSizes[j]):
                    tmp1 = (self.inFile.readline()).split()

        model.ands = [0]*model.num_ands
        for i in range(0,model.num_ands):
            args,err = self.validateInput(3,'Invalid model definition - Ands',verbose)
            if err == 0:
                model.ands[i] = ag.aiger_and(int(args[0]),int(args[1]),int(args[2]),i)
                gateList[int(int(args[0])/2)] = model.ands[i]

        # Connect all the gate inputs up
        for i in range(0,model.num_inputs):
            model.inputs[i].connect(gateList)
  
        for i in range(0,model.num_latches):
            model.latches[i].connect(gateList)

        for i in range(0,model.num_outputs):
            model.outputs[i].connect(gateList)

        for i in range(0,model.num_bad):
            model.bad[i].connect(gateList)

        for i in range(0,model.num_constraints):
            model.constraint[i].connect(gateList)
        
        for i in range(0,model.num_ands):
            model.ands[i].connect(gateList)
            
        self.procModelNames(model)
        
        #Get a count of the controllable InputStates
        for i in range(0,model.num_inputs):
            if model.inputs[i].controlled == True:
                model.num_inputsCtl += 1
                
#--------------------------------------------------------------------------------------
              
    def getStim(self):
        
        args = (self.inFile.readline()).split()
        
        return args

#--------------------------------------------------------------------------------------
           
@dataclass
class Model:

    stepNum         = 0
    maxvar          = 0
    num_inputs      = 0
    num_inputsCtl   = 0
    num_latches     = 0
    num_outputs     = 0
    num_ands        = 0
    num_bad         = 0
    num_constraints = 0
    num_justice     = 0
    num_fairness    = 0

    inputs     = [] # [0..num_inputs]
    latches    = [] # [0..num_latches]
    outputs    = [] # [0..num_outputs]
    bad        = [] # [0..num_bad]
    constraint = [] # [0..num_constraints]
    ands       = [] # [0..num_ands]

    def _init_(self):
        pass
    
    def initModel(self):
        self.stepNum = 0
        self.transTable = tt.aigTransionTable(self.num_latches,self.num_inputs)
        for i in range(0,self.num_latches):
            self.latches[i].resetGate()
                    
    def validateInput(self,args):
        
        err = 0
        if len(args) == self.num_inputs:
            current = [0] * self.num_inputs
            for i in range (self.num_inputs):
                if validInput.issuperset(args.rstrip()):   
                    current[i] = int(args[i])
                else:
                    print('invalid characters in input string')
                    err = -1
                    
        else:
            sys.exit('invalid input string length. Expected {:d} Got {:d} {:s}'.format(self.num_inputs,len(args),args))

        return current,err
        
    def getCurVal(self,lit):
        val = self.current[int(lit/2)]
        if lit%2 != 0:
            val = int(bin(val+1)[-1])
        
        return val
            
    def step(self,args):
        
        for i in range(0,self.num_inputs):
            self.inputs[i].prepStep()
            
        for i in range(0,self.num_latches):
            self.latches[i].prepStep()

        for i in range(0,self.num_ands):            
            self.ands[i].prepStep()
        
        stim,err = self.validateInput(args)  

        # Process the input stimuli
        for i in range(0,self.num_inputs):
            self.inputs[i].curVal = stim[i]

        # Process the latches
        curState  = ''
        nextState = ''
        for i in range(0,self.num_latches):
            self.latches[i].step()
            curState += ("{:1d}".format(self.latches[i].curVal))
            nextState += ("{:1d}".format(self.latches[i].nextVal))
        curState  = int(curState,2)
        nextState = int(nextState,2)
        
        # Process the and gates
        for i in range(0,self.num_ands):
            self.ands[i].step()
            
         # Process the output gates
        for i in range(0,self.num_outputs):
            self.outputs[i].step()

         # Process the bad states
        bad = 0
        for i in range(0,self.num_bad):
            self.bad[i].step()
            if self.bad[i].curVal > 0:
                bad = 1

         # Process the constrained states (negative logic -> 1 = constraint holds)
        constraint = 0
        for i in range(0,self.num_constraints):
            self.constraint[i].step()
            if self.constraint[i].curVal == 0:
                constraint = 1

        self.stepNum += 1
        
        self.transTable.updateTransTable(curState,nextState,int(args,2),bad)
        
        return self.stepNum
        
    def printSelf(self):
        print('Model')
        print('-----')
        print('maxvar          = ',self.maxvar)
        print('num_inputs      = ',self.num_inputs)
        print('  controlled    = ',self.num_inputsCtl)
        print('num_latches     = ',self.num_latches)
        print('num_outputs     = ',self.num_outputs)
        print('num_bad         = ',self.num_bad)
        print('num_constraints = ',self.num_constraints)
        print('num_ands        = ',self.num_ands)
        
        for i in range(0,self.num_inputs):
            self.inputs[i].printSelf()
            
        for i in range(0,self.num_latches):
            self.latches[i].printSelf()
            
        for i in range(0,self.num_outputs):
            self.outputs[i].printSelf()
            
        for i in range(0,self.num_bad):
            self.bad[i].printSelf()
            
        for i in range(0,self.num_constraints):
            self.constraint[i].printSelf()
                        
        for i in range(0,self.num_ands):
            self.ands[i].printSelf()
        
    def printState(self,pOptions,stepNum=0):
    
        status = self.getState()
        
        outStr = self.stateStr(pOptions[1],pOptions[2])
        
        if pOptions[0] == True:
            outStr = "{:4d} ".format(stepNum) + outStr
                        
        print(outStr)

    def stateStr(self,pAStates = True,pHistory = True):
    
        status = self.getState()

        statusStr = ''
        
        statusStr += status["latches_now"]
        statusStr += ' '
        statusStr += status["inputs"]
        statusStr += ' '
        statusStr += status["outputs"]
        statusStr += ' '
        statusStr += status["bad"]
        statusStr += ' '
        statusStr += status["constraint"]
        statusStr += ' '
        statusStr += status["latches_next"]
        statusStr += ' '
        
        if pAStates == True:
            statusStr += status["ands"]
            statusStr += ' '
            
        if pHistory == True:
            statusStr += status["latches_seen"]
            statusStr += ' '
            
            statusStr += status["states_seen"]
       
        return statusStr

    def getState(self):
    
        states = {}
        
        statusStr = ''
        for i in range(0,self.num_latches):
            statusStr += ("{:1d}".format(self.latches[i].curVal))
        states['latches_now'] = statusStr

        statusStr = ''
        for i in range(0,self.num_inputs):
            statusStr += ("{:1d}".format(self.inputs[i].curVal))
        states['inputs'] = statusStr
            
        statusStr = ''
        for i in range(0,self.num_outputs):
            statusStr += ("{:1d}".format(self.outputs[i].curVal))
        states['outputs'] = statusStr
            
        statusStr = ''
        for i in range(0,self.num_bad):
            statusStr += ("{:1d}".format(self.bad[i].curVal))
        states['bad'] = statusStr
            
        statusStr = ''
        for i in range(0,self.num_constraints):
            statusStr += ("{:1d}".format(self.constraint[i].curVal))
        states['constraint'] = statusStr

        statusStr = ''
        for i in range(0,self.num_latches):
            statusStr += ("{:1d}".format(self.latches[i].nextVal))
        states['latches_next'] = statusStr
            
        statusStr = ''
        for i in range(0,self.num_ands):
            statusStr += ("{:1d}".format(self.ands[i].curVal))            
        states['ands'] = statusStr
            
        statusStr = ''
        for i in range(0,self.num_latches):
            statusStr += ("{:02b}".format(self.latches[i].statesSeen))
        states['latches_seen'] = statusStr
            
        statusStr = ''
        for i in range(0,self.num_ands):
            statusStr += ("{:04b}".format(self.ands[i].statesSeen,''))
        states['states_seen'] = statusStr
       
        return states

    def getStats(self):
        
        stats = {}
        stats['maxvar'] = self.maxvar
        stats['inputs'] = self.num_inputs
        stats['controlled'] = self.num_inputsCtl
        stats['latches'] = self.num_latches
        stats['outputs'] = self.num_outputs
        stats['bad']     = self.num_bad
        stats['constraing'] = self.num_constraints
        stats['ands']    = self.num_ands
        
        return stats
        
    def writeGraph(self,outfile):
        
        f = open(outfile,"w")

        f.write('digraph "{}" {{\n'.format(outfile))

        for input in self.inputs:
            f.write(input.dot('blue'))

        for latch in self.latches:
            f.write(latch.dot('magenta'))

        for output in self.outputs:
            f.write(output.dot('blue'))

        for gate in self.ands:
            f.write(gate.dot('black'))

        for gate in self.bad:
            f.write(gate.dot('red'))

        for gate in self.constraint:
            f.write(gate.dot('green'))
        
        f.write('}\n')
        f.close()      
                 
def main():

    verbose0 = False
    verbose1 = False
    printSM  = False
    printDot = False
    graphDot = False
    skipStim = False
    pOptions = [False] * 3

    parser = argparse.ArgumentParser()
    parser.add_argument('-m', type=str, default='', help='Model Filename')
    parser.add_argument('-s', type=str, default='', help='Stim Filename')
    parser.add_argument('-v0', action='store_true', help='Model Statistics')
    parser.add_argument('-v1', action='store_true', help='Model Output')
    parser.add_argument('-p0', action='store_true', help='Print Option: Include simulation step')
    parser.add_argument('-p1', action='store_true', help='Print Option: Include and gate states')
    parser.add_argument('-p2', action='store_true', help='Print Option: Include coverage')
    parser.add_argument('-sm', action='store_true', help='Print Inferred State Machine Transition Table')
    parser.add_argument('-d',  action='store_true', help='Print State Machine dot file')
    parser.add_argument('-g',  action='store_true', help='Print AIGER Graph dot file')
    
    args = parser.parse_args()
    
    if args.m == '':
        sys.exit('No model file provided')
    else:
        modelFile = args.m
    
    if args.s == '':
        print('No stim file provided')
        skipStim = True
    else:
        stimFile = args.s

    if args.v0 == True:
        verbose0 = True
    
    if args.v1 == True:
        verbose1 = True
        
    if args.p0 == True:
        pOptions[0] = True
         
    if args.p1 == True:
        pOptions[1] = True
        
    if args.p2 == True:
        pOptions[2] = True
        
    if args.sm == True:
        printSM = True
   
    if args.d == True:
        printDot = True
        
    if args.g == True:
        graphDot = True
        
    model = Model()

    reader = Reader()
    reader.openFile(modelFile)
    reader.readHeader(model)
    reader.readModel(model)

    if verbose0 == True:
        model.printSelf()
        
    model.initModel()

    if skipStim != True:
        reader = Reader()
        reader.openFile(stimFile)

        done = False
    
        while done != True:
            stim = reader.getStim()
            if len(stim) > 0:
                if stim[0] == '.':
                    done = True
                else:
                    stepNum = model.step(stim[0])
                    if verbose1 == True:
                        model.printState(pOptions,stepNum)
            
            else:
                print('Stim file not properly terminated. Last line should only contain a period')
                done = True

    if printSM == True:
        model.transTable.printTable()
        
    if printDot == True:
        model.transTable.printDotFile(os.path.splitext(modelFile)[0] + '.dot')
        
    if graphDot == True:
        model.writeGraph(os.path.splitext(modelFile)[0] + 'Graph.dot')
    
if __name__== "__main__":
    main()
