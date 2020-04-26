import sys
import argparse
import numpy as np
import random as rd
import SampleGame as sg
import SampleGame2 as sg2
import SafetyGame1 as sf1
import SafetyGame2 as sf2
import TemperatureGame as tg

# Parameters

p_alpha = 0.1;    # learning rate
p_epsilon = 0.1;  # choose random action with epsilon probability
p_lambda = 0.999; # discount factor

n_episodes = 10000;
n_steps = 100;
n_plays = 10;

qFile = 'q.txt'

import csv

# This procedure is used to read in a comma delimited file that was created by Matlab.
# It's here for use in testing code against a Matlab original version. 
def getQ(game,filename):
    
    q = np.empty([game.get_n_observations(),game.get_n_max_actions() * game.get_n_min_actions()])
    
    row = 0
    f = open(filename)
    for line in csv.reader(f):
        q[row] = [float(i) for i in line]
        row += 1

    return q
        
# The original algorithm uses the array index as a key part of the equation. The original was written in Matlab
# with an array index from 1 to n_observations. Here we create the same 3D array but we need to add a row of zeros
# to realign the array to match the Matlab numbering.
def randQ(game):

    q = np.random.rand(game.get_n_observations(), game.get_n_max_actions(), game.get_n_min_actions())

    return q


def minimax_q(game, maxepisodes = 10000, maxsteps = 100 ):
    
    rd.seed()
    
    if maxepisodes < 1 or not isinstance(maxepisodes, int):
        print('The maximum number of episodes must be a positive integer')
        return -1
    
    if maxsteps < 1 or not isinstance(maxsteps, int):
        print('The maximum number of steps must be a positive integer')
        return -1
        
    # For testing purposes the Q matrix can be read from a file to provide a constant
    # data source for repeatability.
    Q = randQ(game)
#    Q = getQ(qFile)

    for ep_len in range(0,maxepisodes):
        curr_observation = game.reset()
        
        # Choose actions for each player
        for step in range(0,maxsteps):
            
            # Choose p_epsilon-greedy action for the Max Player
            if rd.random() < p_epsilon:
                
                # Choose a random Max action
                max_action = rd.randint(0,game.get_n_max_actions()-1)
            else:
                # Choose a Q-maximin action for Max
#                 print('1',Q[curr_observation,:,:])
#                 print('2',np.min(Q[curr_observation,:,:],axis=1))
#                 print('3',np.max(np.min(Q[curr_observation,:,:],axis=1)))
                max_action = np.argmax(np.min(Q[curr_observation,:,:],axis=1))
                
            # Choose p_epsilon-greedy action for the Min Player
            if rd.random() < p_epsilon:
                
                # Choose a random Min action
                min_action = rd.randint(0,game.get_n_min_actions()-1)
            else:
                # Choose a Q-Maximin action for Min
                min_action = np.argmin(Q[curr_observation,max_action,:])
                
            next_observation, reward, done = game.step(max_action, min_action)
            
#            print(curr_observation, next_observation, reward,max_action, min_action)
            
            Q[curr_observation, max_action, min_action] = (1 - p_alpha)* Q[curr_observation, max_action, min_action] \
                                                        + (p_alpha) * (reward + p_lambda * np.argmax(np.min(Q[next_observation,:,:],axis=1)))

            if done == True:
                break
            
            curr_observation = next_observation
            
             
        if ep_len%round(maxepisodes/100) == 0:
            print('.',end='')
            
    print('')
    return Q
    
def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-g', type=str, default='T', help='Game type')
    parser.add_argument('-e', type=int, default=10000, help='Max Episodes')
    parser.add_argument('-s', type=int, default=100, help='Max Steps')
    
    args = parser.parse_args()
    
    if args.g == 'T' :
        g = tg.TemperatureGame()
    elif args.g == 'Sf1':
        g = sf1.SafetyGame1()
    elif args.g == 'Sf2':
        g = sf2.SafetyGame2()
    elif args.g == 'Sg':
        g = sg.SampleGame()
    elif args.g == 'Sg2':
        g = sg2.SampleGame2()
            
    print('Max Episodes = {:d}\nMax Steps = {:d}'.format(args.e,args.s))
    
    Q = minimax_q(g, args.e, args.s)

    print('\nOptimal Policy: ')

    for state in range(0,g.get_n_observations()):
        max_action = np.argmax(np.min(Q[state,:,:],axis=1))
        min_action = np.argmin(Q[state,max_action,:])
        print('State: {:3} Max Action: {:3} Min Action: {:3}'.format(state,max_action,min_action))
    
    print('\nQuick Play')
    curr_state = g.reset()
    for play in range(0,n_plays):
        max_action = np.argmax(np.min(Q[curr_state,:,:],axis=1))
        min_action = np.argmin(Q[curr_state,max_action,:])
        next_state, reward, done = g.step(max_action, min_action)
        print('{:3}: State: {:2} Play: {:1}{:1} Reward: {:2} New State: {:2}'.format(play,curr_state,max_action,min_action,reward,next_state))
        curr_state = next_state
        
if __name__== "__main__":
    main()
   