# AIGER
Python version of tools to work with AIG formatted files<br />


There are two versions of the code here. One is a standard py file. The other is a Jupyter notebook. The model and stim files for the jupyter notebook are hardcoded in the first cell.<br />

For the py file:<br />

python aigsim.py -h<br />
usage: aigsim.py [-h] [-m M] [-s S] [-v0] [-v1] [-v2]<br />

optional arguments:<br />
  -h, --help  show this help message and exit<br />
  -m M        Model Filename<br />
  -s S        Stim Filename<br />
  -v0         Model Statistics<br />
  -v1         Model Output<br />
  -v2         Model Output with and gates<br />

A standard invocation:<br />

python aigsim.py -m modelFile.aag -s stimFile.txt<br />

Verbose option 0 prints model statistics:<br />

Model
maxvar      =  7<br />
num_inputs  =  2<br />
num_latches =  2<br />
num_outputs =  1<br />
num_ands    =  3<br />
aiger_symbol - Type: Input  lit:  2                    input: I0      name:I0        
aiger_symbol - Type: Input  lit:  4                    input: I1      name:I1        
aiger_symbol - Type: Latch  lit: 12 next:  6 reset:  0 input: A0      name:L0        
aiger_symbol - Type: Latch  lit: 10 next:  8 reset:  0 input: A1      name:L1        
aiger_symbol - Type: Output lit: 14                    input: A2      name:O0        
aiger_symbol - Type: And    lit:  6 rhs0:  2  rhs1:  4 input: I0  I1  name:A0        
aiger_symbol - Type: And    lit:  8 rhs0:  4  rhs1:  7 input: I1  A0* name:A1        
aiger_symbol - Type: And    lit: 14 rhs0: 11  rhs1: 12 input: L1* L0  name:A2        

Verbose option 1 prints model state at the end of each step of execution where<br />
Column 1 = latches before step<br />
Column 2 = input stimuli<br />
Column 3 = output states<br />
Column 4 = latches after step<br />

Example output from aigTestSMV2.aag.txt:<br />
00 11 0 10 <br />
10 11 1 10 <br />
10 10 1 00 <br />
00 10 0 00 <br />
00 11 0 10 <br />
10 00 1 00 <br />
00 10 0 00 <br />

Verbose option 2 prints model state after the end of each step of execution with the addition of the and gate states:<br />
Column 1 = model step<br />
Column 2 = latches before step<br />
Column 3 = input stimuli<br />
Column 4 = output states<br />
Column 5 = latches after step<br />
Column 6 = and gate states<br />

Example output from aigTestSMV2.aag.txt:<br />
   0 00 11 10 0 100 <br />
   1 10 11 10 1 101 <br />
   2 10 10 00 1 001 <br />
   3 00 10 00 0 000 <br />
   4 00 11 10 0 100 <br />
   5 10 00 00 1 001 <br />

# Model Files
The following model files are provided in the examples directory:
aigTestSMV2.aag.txt             - A simple toggling latch with enable. Stim file = stim1.txt
counter.aag.                    - An AIGER benchmark file for a complex counter. Stim file = stimCounter.txt
random_n_19_1_2_16_14_2_abc.aag - An AIGER competition file with over 1M and gates. Stim file = stim3.txt

