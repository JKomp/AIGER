from dataclasses import dataclass

# Implementation of a very stripped down version of the C program aigsim

# Source Files
modelFile = 'aigTestSMV2.aag.txt'
stimFile  = 'stim1.txt'

STORE_PATH = '/Users/john/Jupyter/Machine Learning'

validInput = {"0","1"}

from dataclasses import dataclass

@dataclass
class aiger_symbol:

    lit    = 0  # Number assigned to this gate as literal [0..2*maxvar+1]
    next   = 0  # Number of gate connected to this gate's input as literal - latches only
    reset  = 0  # used only for latches
    type   = '' # What type of object is this    - aigsim new parameter
    oldVal = 0  # The previous value of this symbol - aigsim new parameter
    name   = ''

    def _init_(self):
        pass

    # Build a translation table from original model file encoding to a standard
    # ordering of inputs, latches, ands. Note that if the lit passed in was inverted
    # (i.e. was an odd number) then the table is filled in in opposite order.        

    def encoder(self,counter,curCntr,typeName):
        
        symbol = aiger_symbol()
        if self.lit % 2 == 0:
            symbol.lit = curCntr
            counter[self.lit] = curCntr
            counter[self.lit+1] = curCntr+1
        else:
            symbol.lit = curCntr + 1      
            counter[self.lit-1] = curCntr
            counter[self.lit] = curCntr+1
            
        symbol.type = typeName
        curCntr += 2

        return symbol,counter,curCntr
 
    def printSelf(self):
        print('aiger_symbol - Type: {:6} lit: {:2} next: {:2} reset: {:2} name:{:10}'.format(self.type,self.lit,self.next,self.reset,self.name))                                

@dataclass
class aiger_and:
    
    lhs  = 0  # as literal [2..2*maxvar], even
    rhs0 = 0  # as literal [0..2*maxvar+1]
    rhs1 = 0  # as literal [0..2*maxvar+1] 

    def _init_(self):
        pass
    
    # Build a translation table from original model file encoding to a standard
    # ordering of inputs, latches, ands. Note that if the lit passed in was inverted
    # (i.e. was an odd number) then the table is filled in in opposite order.        

    def encoder(self,counter,curCntr,typeName):
        
        symbol = aiger_and()
        if self.lhs % 2 == 0:
            symbol.lhs = curCntr
            counter[self.lhs] = curCntr
            counter[self.lhs+1] = curCntr+1
        else:
            symbol.lhs = curCntr + 1      
            counter[self.lhs-1] = curCntr
            counter[self.lhs] = curCntr+1
            
        symbol.type = typeName
        curCntr += 2

        return symbol,counter,curCntr

    def printSelf(self):        
        print('aiger_symbol - Type:    And lhs: {:2} rhs0: {:2}  rhs1: {:2}'.format(self.lhs,self.rhs0,self.rhs1))
        
@dataclass
class Reader:
    
    inFile = ''
    
    def _init_(self):
        pass
    
    def openFile(self,file):
        
        self.inFile = open(file)
        
    def readHeader(self,model):
        
        args = (self.inFile.readline()).split()
        
        if args[0] != 'aag':
            return -1
        
        model.maxvar      = int(args[1])
        model.num_inputs  = int(args[2])
        model.num_latches = int(args[3])
        model.num_outputs = int(args[4])
        model.num_ands    = int(args[5])
        
        return 0
    
    def validateInput(self,numArgs,errStr,verbose):
        
        args = (self.inFile.readline()).split()
        
        err = 0
        if len(args) != numArgs:
            print(errStr)
            err = -1
        
        if verbose == True:
            print(args)
            
        return args,err

    def readModel(self,model):
        
        verbose = False
        
        model.inputs = [0]*model.num_inputs
        for i in range(0,model.num_inputs):
            args,err = self.validateInput(1,'Invalid model definition - Input',verbose)
            if err == 0:
                symbol = aiger_symbol()
                symbol.lit = int(args[0])
                symbol.type = ' Input'
                model.inputs[i] = symbol
                 
        model.latches = [0]*model.num_latches
        for i in range(0,model.num_latches):
            args,err = self.validateInput(3,'Invalid model definition - Latches',verbose)
            if err == 0:
                symbol = aiger_symbol()
                symbol.lit   = int(args[0])
                symbol.next  = int(args[1])
                symbol.reset = int(args[2])
                symbol.type  = ' Latch'
                model.latches[i] = symbol
        
        model.outputs = [0]*model.num_outputs
        for i in range(0,model.num_outputs):
            args,err = self.validateInput(1,'Invalid model definition - Output',verbose)
            if err == 0:
                symbol = aiger_symbol()
                symbol.lit  = int(args[0])
                symbol.type = 'Output'
                model.outputs[i] = symbol
        
        model.ands = [0]*model.num_ands
        for i in range(0,model.num_ands):
            args,err = self.validateInput(3,'Invalid model definition - Ands',verbose)
            if err == 0:
                symbol = aiger_and()
                symbol.lhs  = int(args[0])
                symbol.rhs0 = int(args[1])
                symbol.rhs1 = int(args[2])
                model.ands[i] = symbol

    def reencode(self,model):
        
        newModel = Model()
        newModel.maxvar      = model.maxvar
        newModel.num_inputs  = model.num_inputs
        newModel.num_latches = model.num_latches
        newModel.num_outputs = model.num_outputs
        newModel.num_ands    = model.num_ands
 
        counter = [0] * ((model.maxvar*2) + 2)
        curCntr = 2
        
        newModel.inputs = [0]*model.num_inputs
        for i in range(0,model.num_inputs):
            symbol,counter,curCntr = model.inputs[i].encoder(counter,curCntr,'Input')
            newModel.inputs[i] = symbol

        newModel.latches = [0]*model.num_latches
        for i in range(0,model.num_latches):
            symbol,counter,curCntr = model.latches[i].encoder(counter,curCntr,'Latch')
            newModel.latches[i] = symbol

        newModel.ands = [0]*model.num_ands
        for i in range(0,model.num_ands):
            symbol,counter,curCntr = model.ands[i].encoder(counter,curCntr,'And')
            newModel.ands[i] = symbol

        newModel.outputs = [0]*model.num_outputs
        for i in range(0,model.num_outputs):
            symbol = aiger_symbol()
            symbol.lit = counter[model.outputs[i].lit]
            symbol.type = 'Output'
            newModel.outputs[i] = symbol

        for i in range(0,model.num_latches):
            newModel.latches[i].next = counter[model.latches[i].next]
            newModel.latches[i].reset = counter[model.latches[i].reset]

        for i in range(0,model.num_ands):
            newModel.ands[i].rhs0 = counter[model.ands[i].rhs0]
            newModel.ands[i].rhs1 = counter[model.ands[i].rhs1]

        return newModel
    
    def getStim(self):
        
        args = (self.inFile.readline()).split()
        
        return args
           
@dataclass
class Model:

    stepNum     = 0
    maxvar      = 0
    num_inputs  = 0
    num_latches = 0
    num_outputs = 0
    num_ands    = 0

    inputs  = [] # [0..num_inputs]
    latches = [] # [0..num_latches]
    outputs = [] # [0..num_outputs]

    ands    = [] # [0..num_ands]
    
    current = [] # [0..maxvar+1] - holds current output of each gate

    def _init_(self):
        pass
    
    def initModel(self):
        self.stepNum = 0
        self.current = [0] * (self.maxvar + 1) # for index simplicity, index 0 is unused
        
        # Initialize the latches    
        # - Note this code does not support reset reset values outside {0,1}.
        
        for i in range(0,self.num_latches):
            self.current[int((self.latches[i].lit)/2)] = self.latches[i].reset
        
    # Does not support ground or don't care values
    
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
            print('invalid input string length')
            err = -1

        return current,err
        
    def getCurVal(self,lit):
        val = self.current[int(lit/2)]
        if lit%2 != 0:
            val = ~val
        
        return val
    
    def step(self,args,verbose):
        
        stim,err = self.validateInput(args)  
        
        # Process the input stimuli
        for i in range(0,self.num_inputs):
            self.current[i+1] = stim[i]
            
        # Process the and gates
        for i in range(0,self.num_ands):
            lhs = self.getCurVal(self.ands[i].rhs0)
            rhs = self.getCurVal(self.ands[i].rhs1)
            self.current[int((self.ands[i].lhs)/2)] = lhs & rhs
            
        # Process the latches
        nextLatch = [0]*self.num_latches
        for i in range(0,self.num_latches):
            nextLatch[i] = self.getCurVal(self.latches[i].next)
            self.latches[i].oldVal = self.getCurVal(self.latches[i].lit)
            
        for i in range(0,self.num_latches):
            self.current[int(self.latches[i].lit/2)] = nextLatch[i]
            
        if verbose == True:
            print(self.stepNum,self.current)
        self.stepNum += 1
    
    def printResults(self):
        
        for i in range(0,self.num_latches):
            print('{:1}'.format(self.latches[i].oldVal),end='')
        print(' ',end='')

        for i in range(0,self.num_inputs):
            print('{:1}'.format(self.getCurVal(self.inputs[i].lit)),end='')
        print(' ',end='')
            
        for i in range(0,self.num_outputs):
            print('{:1}'.format(self.getCurVal(self.outputs[i].lit)),end='')
        print(' ',end='')
        
        for i in range(0,self.num_latches):
            print('{:1}'.format(self.getCurVal(self.latches[i].lit)),end='')

        print('')
        
    def printSelf(self):
        print('Model')
        print('-----')
        print('maxvar      = ',self.maxvar)
        print('num_inputs  = ',self.num_inputs)
        print('num_latches = ',self.num_latches)
        print('num_outputs = ',self.num_outputs)
        print('num_ands    = ',self.num_ands)
        
        for i in range(0,self.num_inputs):
            self.inputs[i].printSelf()
            
        for i in range(0,self.num_latches):
            self.latches[i].printSelf()
            
        for i in range(0,self.num_outputs):
            self.outputs[i].printSelf()
            
        for i in range(0,self.num_ands):
            self.ands[i].printSelf()
        
model = Model()

reader = Reader()
reader.openFile(modelFile)
reader.readHeader(model)
reader.readModel(model)

# model.printSelf()
model = reader.reencode(model)
print('After reencoding the inputs:')
model.printSelf()
model.initModel()

reader = Reader()
reader.openFile(stimFile)

done = False
verbose = True

while done != True:
    stim = reader.getStim()
    if len(stim) > 0:
        if stim[0] == '.':
            done = True
        else:
            model.step(stim[0],False)
            if verbose == True:
                model.printResults()
            
    else:
        print('Stim file not properly terminated. Last line should only contain a period')
        done = True

