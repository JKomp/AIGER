import sys
import argparse
import numpy as np
import random as rd
import csv
import SafetyGame1 as sg
import SampleGame as ag

# Parameters

p_alpha = 0.1;    # learning rate
p_epsilon = 0.1;  # choose random action with epsilon probability
p_lambda = 0.999; # discount factor

n_episodes = 10000;
n_steps = 1000;


def minimax_q(game, maxepisodes = 10000, maxsteps = 100 ):

    rd.seed()

    if maxepisodes < 1 or not isinstance(maxepisodes, int):
        sys.exit('The maximum number of episodes must be a positive integer')

    if maxsteps < 1 or not isinstance(maxsteps, int):
        sys.exit('The maximum number of steps must be a positive integer')

    # For testing purposes the Q matrix can be read from a file to provide a constant
    # data source for repeatability.
    Q = np.random.rand(game.get_n_states(), game.get_n_actions())
    
    for ep_len in range(0,maxepisodes):
        curr_state  = game.init()
        curr_player = game.player(curr_state)

        # Choose actions for each player
        for step in range(0,maxsteps):

            # Choose p_epsilon-greedy action
            if rd.random() < p_epsilon:

                # Choose a random Max action
                next_action = rd.randint(0,game.get_n_actions()-1)
            else:
                if curr_player == 0:
                    next_action = np.argmax(Q[curr_state,:],axis=0)
                else:
                    next_action = np.argmin(Q[curr_state,:],axis=0)

            next_state, reward, done = game.step(curr_state,next_action)
            next_player = game.player(next_state)

            if curr_player == 0:
                Q[curr_state, next_action] = p_alpha * Q[curr_state, next_action] \
                                           + (1 - p_alpha) * (reward + p_lambda * np.max(Q[next_state,:],axis=0))
            else:
                Q[curr_state, next_action] = p_alpha * Q[curr_state, next_action] \
                                           + (1 - p_alpha) * (reward + p_lambda * np.min(Q[next_state,:],axis=0))

            if done == True:
                break

            curr_state = next_state
            curr_player = next_player


        if ep_len%round(maxepisodes/100) == 0:
            print('.',end='')

    print('')
    return Q

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-g', type=str, default='SafetyGame1', help='Game Type')
    
    args = parser.parse_args()
    
    print('\nRunning game: {:s}\n'.format(args.g))
    if args.g == 'SafetyGame1':    
        game = sg.SafetyGame()
    elif args.g == 'SampleGame':
        game = ag.SampleGame()
    else:
        sys.exit('Invalid game name')

    Q = minimax_q(game,n_episodes,n_steps)

    for iState in range(0,game.get_n_states()):
        if game.player(iState) == 0:
           action = np.argmax(Q[iState,:],axis=0)
           print('state: {:2d} player: {:2d} action: {:2d}'.format(iState,game.player(iState),action))
        else:
           action = np.argmin(Q[iState,:],axis=0)
           print('state: {:2d} player: {:2d} action: {:2d}'.format(iState,game.player(iState),action))
           
    print(Q)
    
if __name__== "__main__":
    main()
