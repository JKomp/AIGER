from dataclasses import dataclass
import math
import re

class aiger_symbol:

    lit        = 0  # Number assigned to this gate by the model file, format: [0..2*maxvar+1]
    gID        = 0  # Gate ID number. Assumed use is to sequentially number gates of a same class
    type       = '' # What type of object is this 
    gName      = '' # Internally generated short name of gate
    modName    = '' # Name give to the gate by the model file
    myInput    = '' # The gate that feeds this one (builds a binary tree of the model gates)
    myInputNeg = False # Is the feeder gate negated
    curVal     = 0  # The current gate value
    statesSeen = 0  # Keeps a running list of which input states the gate has seen
	
    def __init__(self,lit,typeName,gID=0,gName=''):
        self.lit = lit
        self.type = typeName
        if self.gName == '':
            self.gName = typeName[0] + str(gID)
 
    def connect(self,gateList):
        self.myInput = gateList[int(self.lit/2)]
        if self.lit % 2 != 0:
            self.myInputNeg = True
            
    def resetGate(self):
        pass
          
    def setModName(self,mName):
        self.modName = mName
        
    def prepStep(self):
        self.oldVal = self.curVal
        self.curVal = float('nan')
          
    def step(self):
        return(self.curVal)
        
    def printSelf(self):
        conStr = self.myInput.gName
        if self.myInputNeg == True:
           conStr += '*'
        else:
           conStr += ' '
           
        print('Type: {:6} lit: {:3}                      input: {:4}      name:{:4} {:20}'.format(self.type,self.lit,conStr,self.gName,self.modName))                                

#--------------------------------------------------------------------------------------

class aiger_const(aiger_symbol):

    def prepStep(self):
        self.oldVal = self.curVal

#--------------------------------------------------------------------------------------

class aiger_input(aiger_symbol):

    controlled = False
    
    def setModName(self,mName):
        super().setModName(mName)
        
        if re.search('control', mName, re.IGNORECASE) and not re.search('uncontrol', mName, re.IGNORECASE):
            self.controlled = True

#--------------------------------------------------------------------------------------

class aiger_output(aiger_symbol):

          
    def step(self):
        self.curVal = self.myInput.step()
        return(self.curVal)

#--------------------------------------------------------------------------------------
# - Note this code does not support reset reset values outside {0,1}.

class aiger_latch(aiger_symbol):

    next   = 0  # Number of gate connected to this gate's input as literal - latches only
    reset  = 0  # The initial state of the latch upon reset/startup
    nextVal = 0

    def __init__(self,lit,input,reset,gID=0,gName=''):
        super().__init__(lit,'Latch',gID,gName)
        self.next = input
        self.reset = reset
        self.curVal = reset
        self.nextVal = reset
        
    def connect(self,gateList):
        self.myInput = gateList[int(self.next/2)]
        if self.next % 2 != 0:
            self.myInputNeg = True

    def resetGate(self):
        self.curVal = self.reset
        self.nextVal = self.reset
        
    def prepStep(self):
        self.oldVal = self.curVal
        self.curVal = float('nan')

    def step(self):
        if math.isnan(self.curVal):
            self.curVal  = self.nextVal

            self.nextVal = self.myInput.step()
            if self.myInputNeg == True:
                self.nextVal = int(bin(self.nextVal+1)[-1])
                
            self.statesSeen = self.statesSeen | 0x1 << self.curVal
            
        return self.curVal
        
    def printSelf(self):
        conStr = self.myInput.gName
        if self.myInputNeg == True:
           conStr += '*'
        else:
           conStr += ' '
           
        print('Type: {:6} lit: {:3} next: {:3} reset: {:3} input: {:4}      name:{:4} {:20}'.format(self.type,self.lit,self.next,self.reset,conStr,self.gName,self.modName))                                

#--------------------------------------------------------------------------------------

class aiger_and(aiger_symbol):
    
    rhs0 = 0  # as literal [0..2*maxvar+1]
    rhs1 = 0  # as literal [0..2*maxvar+1] 
    in0  = 0
    in0Neg = False
    in1  = 0
    in1Neg = False

    def __init__(self,lit,rhs0,rhs1,gID=0,gName=''):
        super().__init__(lit,'And',gID,gName)
        self.rhs0 = rhs0
        self.rhs1 = rhs1

    def connect(self,gateList):
        self.in0 = gateList[int(self.rhs0/2)]
        if self.rhs0 % 2 != 0:
            self.in0Neg = True

        self.in1 = gateList[int(self.rhs1/2)]
        if self.rhs1 % 2 != 0:
            self.in1Neg = True

    def step(self):
        if math.isnan(self.curVal):
            rhs0 = self.in0.step()
            if self.in0Neg == True:
                rhs0 = int(bin(rhs0+1)[-1])
            rhs1 = self.in1.step()
            if self.in1Neg == True:
                rhs1 = int(bin(rhs1+1)[-1])
            self.curVal = rhs0 & rhs1

            if rhs1 == 0 and rhs0 == 0:
                self.statesSeen = self.statesSeen | 0x1
            elif rhs1 == 0 and rhs0 == 1:
                self.statesSeen = self.statesSeen | 0x2
            elif rhs1 == 1 and rhs0 == 0:
                self.statesSeen = self.statesSeen | 0x4
            elif rhs1 == 1 and rhs0 == 1:
                self.statesSeen = self.statesSeen | 0x8
          
        return self.curVal

    def printSelf(self):        
        conStr = self.in0.gName
        if self.in0Neg == True:
           conStr += '*'
        
        conStr += ' '*(5-len(conStr))

        conStr += self.in1.gName
        if self.in1Neg == True:
           conStr += '*'
        
        conStr += ' '*(9-len(conStr))

        print('Type: {:6} lit: {:3} rhs0: {:3}  rhs1: {:3} input: {:9} name:{:10}'.format(self.type,self.lit,self.rhs0,self.rhs1,conStr,self.gName))

