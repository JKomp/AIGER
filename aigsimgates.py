from dataclasses import dataclass
import math

class aiger_symbol:

    lit     = 0  # Number assigned to this gate as literal [0..2*maxvar+1]
    gID     = 0  # Gate ID number. Assumed use is to sequentially number gates of a same class
    type    = '' # What type of object is this    - aigsim new parameter
    oldVal  = 0  # The previous gate value        - aigsim new parameter
    curVal  = 0  # The current gate value
    gName   = ''
    myInput = '' # The gate that feeds this one
    myInputNeg = False # Is the feeder gate negated
	
    def __init__(self,lit,typeName,gID=0,gName=''):
        self.lit = lit
        self.type = typeName
        if gName == '':
            self.gName = typeName[0] + str(gID)
 
    def connect(self,gateList):
        self.myInput = gateList[int(self.lit/2)]
        if self.lit % 2 != 0:
            self.myInputNeg = True
          
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
           
        print('aiger_symbol - Type: {:6} lit: {:2}                    input: {:3}     name:{:10}'.format(self.type,self.lit,conStr,self.gName))                                

#--------------------------------------------------------------------------------------

class aiger_const(aiger_symbol):

    def prepStep(self):
        self.oldVal = self.curVal

#--------------------------------------------------------------------------------------

class aiger_input(aiger_symbol):

    pass

#--------------------------------------------------------------------------------------

class aiger_output(aiger_symbol):

          
    def step(self):
        self.curVal = self.myInput.step()
        return(self.curVal)

#--------------------------------------------------------------------------------------

class aiger_latch(aiger_symbol):

    next   = 0  # Number of gate connected to this gate's input as literal - latches only
    reset  = 0
    nextVal = 0

    def __init__(self,lit,input,reset,gID=0,gName=''):
        super().__init__(lit,'Latch',gID,gName)
        self.next = input
        self.reset = reset
        
    def connect(self,gateList):
        self.myInput = gateList[int(self.next/2)]
        if self.next % 2 != 0:
            self.myInputNeg = True

    def prepStep(self):
        self.oldVal = self.curVal
        self.curVal = float('nan')

    def step(self):
        if math.isnan(self.curVal):
            self.curVal  = self.nextVal

            self.nextVal = self.myInput.step()
            if self.myInputNeg == True:
                self.nextVal = int(bin(self.nextVal+1)[-1])
            
        return self.curVal
        
    def printSelf(self):
        conStr = self.myInput.gName
        if self.myInputNeg == True:
           conStr += '*'
        else:
           conStr += ' '
           
        print('aiger_symbol - Type: {:6} lit: {:2} next: {:2} reset: {:2} input: {:3}     name:{:10}'.format(self.type,self.lit,self.next,self.reset,conStr,self.gName))                                

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
           
        return self.curVal

    def printSelf(self):        
        conStr = self.in0.gName
        if self.in0Neg == True:
           conStr += '*'
        else:
           conStr += ' '
           
        conStr += ' ' + self.in1.gName
        if self.in1Neg == True:
           conStr += '*'

        print('aiger_symbol - Type: {:6} lit: {:2} rhs0: {:2}  rhs1: {:2} input: {:7} name:{:10}'.format(self.type,self.lit,self.rhs0,self.rhs1,conStr,self.gName))
