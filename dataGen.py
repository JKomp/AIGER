import sys
import random
import argparse

#usage example: python dataGen.py 5 100 > data1.txt

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', type=int, default=2, help='Number of Inputs to Simulate')
    parser.add_argument('-l', type=int, default=100, help='Length of simulation stream to create')
    
    args = parser.parse_args()

    # the first argument is the number of inputs to simulate
    numInputs = args.i
    
    # the second argument is the length of the simulation
    seqLen = args.l
    
    for i in range(0,seqLen):
    	for j in range(0,numInputs):
    		print(random.randint(0,1),end='')
    	print('')

    print('.\n')
#     if is_rand == 1:
#         upper_bound = int(sys.argv[3])
#         inp_size = random.randint(3, upper_bound)


if __name__== "__main__":
    main()
