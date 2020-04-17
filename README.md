# AIGER
Python version of tools to work with AIG formatted files


There are two versions of the code here. One is a standard py file. The other is a Jupyter notebook. The model and stim files for the jupyter notebook are hardcoded in the first cell.

For the py file:

python aigsim.py -h
usage: aigsim.py [-h] [-m M] [-s S] [-v0] [-v1] [-v2]

optional arguments:
  -h, --help  show this help message and exit
  -m M        Model Filename
  -s S        Stim Filename
  -v0         Model Statistics
  -v1         Model Output
  -v2         Model Output with and gates

A standard invocation:

python aigsim.py -m modelFile.aag -s stimFile.txt

Verbose option 0 prints model statistics:

Model
maxvar      =  7
num_inputs  =  2
num_latches =  2
num_outputs =  1
num_ands    =  3
aiger_symbol - Type: Input  lit:  2                    input: I0      name:I0        
aiger_symbol - Type: Input  lit:  4                    input: I1      name:I1        
aiger_symbol - Type: Latch  lit: 12 next:  6 reset:  0 input: A0      name:L0        
aiger_symbol - Type: Latch  lit: 10 next:  8 reset:  0 input: A1      name:L1        
aiger_symbol - Type: Output lit: 14                    input: A2      name:O0        
aiger_symbol - Type: And    lit:  6 rhs0:  2  rhs1:  4 input: I0  I1  name:A0        
aiger_symbol - Type: And    lit:  8 rhs0:  4  rhs1:  7 input: I1  A0* name:A1        
aiger_symbol - Type: And    lit: 14 rhs0: 11  rhs1: 12 input: L1* L0  name:A2        

Verbose option 1 prints model state at the end of each step of execution where
Column 1 = latches before step
Column 2 = input stimuli
Column 3 = output states
Column 4 = latches after step

Example output from aigTestSMV2.aag.txt:
00 11 0 10
10 11 1 10
10 10 1 00
00 10 0 00
00 11 0 10
10 00 1 00
00 10 0 00

Verbose option 2 prints model state after the end of each step of execution with the addition of the and gate states:
Column 1 = model step
Column 2 = latches before step
Column 3 = input stimuli
Column 4 = output states
Column 5 = latches after step
Column 6 = and gate states

Example output from aigTestSMV2.aag.txt:
   0 00 11 10 0 100
   1 10 11 10 1 101
   2 10 10 00 1 001
   3 00 10 00 0 000
   4 00 11 10 0 100
   5 10 00 00 1 001

# Model Files
The following model files are provided in the examples directory:
aigTestSMV2.aag.txt             - A simple toggling latch with enable. Stim file = stim1.txt
counter.aag.                    - An AIGER benchmark file for a complex counter. Stim file = stimCounter.txt
random_n_19_1_2_16_14_2_abc.aag - An AIGER competition file with over 1M and gates. Stim file = stim3.txt

