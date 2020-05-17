# AIGER
Python version of tools to work with AIG formatted files<br />


There are two versions of the code here. One is a standard py file. The other is a Jupyter notebook. The model and stim files for the jupyter notebook are hardcoded in the first cell.<br />

For the py file:<br />

## From Command Line
```
python aigsim.py -h
usage: aigsim.py [-h] [-m M] [-s S] [-v0] [-v1] [-p0] [-p1] [-p2] [-sm] [-d]

optional arguments:
  -h, --help  show this help message and exit
  -m M        Model Filename
  -s S        Stim Filename
  -v0         Model Statistics
  -v1         Model Output
  -p0         Print Option: Include simulation step
  -p1         Print Option: Include and gate states
  -p2         Print Option: Include coverage
  -sm         Print Inferred State Machine Transition Table
  -d          Print State Machine dot file
  ```
A standard invocation:<br />

`python aigsim.py -m modelFile.aag -s stimFile.txt`

Verbose option `-v0` prints model statistics:<br />

Example output from: `python aigsim.py -m aigTestSMV2.aag.txt -s stim1.txt -v0`
```
maxvar      =  7
num_inputs  =  2
num_latches =  2
num_outputs =  1
num_ands    =  3
aiger_symbol - Type: Input  lit:   2                      input: I0        name:I0   uncontrollable      
aiger_symbol - Type: Input  lit:   4                      input: I1        name:I1   controllable_c0     
aiger_symbol - Type: Latch  lit:  12 next:   6 reset:   0 input: A0        name:L0   latch0              
aiger_symbol - Type: Latch  lit:  10 next:   8 reset:   0 input: A1        name:L1   latch1              
aiger_symbol - Type: Output lit:  14                      input: A2        name:O0                       
aiger_symbol - Type: And    lit:   6 rhs0:   2  rhs1:   4 input: I0  I1    name:A0        
aiger_symbol - Type: And    lit:   8 rhs0:   4  rhs1:   7 input: I1  A0*   name:A1        
aiger_symbol - Type: And    lit:  14 rhs0:  11  rhs1:  12 input: L1* L0    name:A2        
  
```
Verbose option `-v1` with no print options prints model state at the end of each step of execution where<br />
- Column 1 = latches before step<br />
- Column 2 = input stimuli<br />
- Column 3 = output states<br />
- Column 4 = latches after step<br />

Example output from: `python aigsim.py -m aigTestSMV2.aag.txt -s stim1.txt -v0 -v1`
```
00 11 0 10 
10 11 1 10 
10 10 1 00 
00 10 0 00 
00 11 0 10 
10 00 1 00  
```

Adding print option `-p0` prints model state after the end of each step of execution with the addition of the current simulation step:<br />
- Column 1 = model step<br />
- Column 2 = latches before step<br />
- Column 3 = input stimuli<br />
- Column 4 = output states<br />
- Column 5 = latches after step<br />

Example output from: `python aigsim.py -m aigTestSMV2.aag.txt -s stim1.txt -v0 -p0`
```
   1 00 11 0 10 
   2 10 11 1 10 
   3 10 10 1 00 
   4 00 10 0 00 
   5 00 11 0 10 
   6 10 00 1 00 
```
Adding print option `-p1` prints model state after the end of each step of execution with the addition of the and gate states:<br />
- Column 1 = model step<br />
- Column 2 = latches before step<br />
- Column 3 = input stimuli<br />
- Column 4 = output states<br />
- Column 5 = latches after step<br />
- Column 6 = and gate states<br />

Example output from: `python aigsim.py -m aigTestSMV2.aag.txt -s stim1.txt -v0 -p0 -p1`
```
   1 00 11 0 10 100 
   2 10 11 1 10 101 
   3 10 10 1 00 001 
   4 00 10 0 00 000 
   5 00 11 0 10 100 
   6 10 00 1 00 001 
   ```
 
Adding print option `-p2` prints model coverage. Each latch has two bits where the lower bit is having seen a `0` input and the upper bit denotes having seen a `1` input. Each and gate has four bits where the bit represent:<br />
 - `b0` = input pattern `00`
 - `b1` = input pattern `01`
 - `b2` = input pattern `10`
 - `b3` = input pattern `11`

The output columns are defined as:
- Column 1 = model step<br />
- Column 2 = latches before step<br />
- Column 3 = input stimuli<br />
- Column 4 = output states<br />
- Column 5 = latches after step<br />
- Column 6 = and gate states<br />
- Column 7 = latch coverage<br />
- Column 8 = and coverage<br />

**Note:** It is not recommended to use this option with models containing large numbers of and gates.

Example output from: `python aigsim.py -m aigTestSMV2.aag.txt -s stim1.txt -v0 -p0 -p1 -p2`
```
   1 00 11 0 10 100 0101 100000100010
   2 10 11 1 10 101 1101 100000101010
   3 10 10 1 00 001 1101 101001101010
   4 00 10 0 00 000 1101 101001101010
   5 00 11 0 10 100 1101 101001101010
   6 10 00 1 00 001 1101 101101101010
   ```

Print options may be used in any combination. -v1 is required to enable any print option.

The `-sm` option prints the state transition table inferred from the simulation run. It assumes the combination of latch values equates to the unique states of the circuit being simulated. It records the starting state, ending state, and the input value that caused the transition. If a state is never reached during the simulation it will be shown as a '.'. An example output:
```
python aigsim.py -m aigGrant3.aag -s stim2.txt -sm

Transistion Table
------------------

        Input
      ------------
State  11 10 01 00
----- ------------
  0     0  1  0  0
  1     0  3  0  2
  2     0  3  0  2
  3     0  .  0  2
```
  
### Model Files
The following model files are provided in the examples directory:<br />

| Model | Stim File | Description |
| --- | --- | --- |
| `aigTestSMV2.aag.txt` | stim1.txt | A simple toggling latch with enable |
| `counter.aag` | stimCounter.txt | An AIGER benchmark file for a complex counter |
| `runnerGame.aag` | runnerStim1_7.txt | A simple 2 player, concurrent game of a runner and blocker |
| `random_n_19_1_2_16_14_2_abc.aag` | stim3.txt | An AIGER competition file with over 1M and gates |

**Note:** `random_n_19_1_2_16_14_2_abc.aag` is an extremely large model with over 1M gates. Caution recommended on verbose print options used.

## As a module

aigsim.py may also be used as a module. Usage requires the following steps:

- Create a Model object
- Create a Reader to read the model file
- Open and read the model
- Initialize the model
- Feed stimulus to the model

Example:
```
    model = Model()

    reader = Reader()
    reader.openFile(modelFile)
    reader.readHeader(model)
    reader.readModel(model)

    if verbose0 == True:
        model.printSelf()
        
    model.initModel()

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
```
# Data Generation

dataGen.py is a quick script to generate random simulation data. 

Invocation:
```
python ./dataGen.py -h
usage: dataGen.py [-h] [-i I] [-l L]

optional arguments:
  -h, --help  show this help message and exit
  -i I        Number of Inputs to Simulate
  -l L        Length of simulation stream to create
  ```
  The output will be a file containing `L` lines of binary data where each line is `I` digits wide.
  
