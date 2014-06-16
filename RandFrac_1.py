from __future__ import division
import sys                                            
import numpy as np
from random import randrange
import math
import random
import itertools
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.path as path
""" This script does some stuff

    1. Coding random fraction models
    2. Defining our models functions
    3. Creating a module to hold our functions
    
"""


def simple_random_fraction(N, S, sample_size):
    
    RAC_samples = [] # this is a list of RACs, and each RAC is a list   ...a list of lists            
    while len(RAC_samples) < sample_size:
    
        RAC = [N]
        
        while len(RAC) < S:
            
            sp1_ab = random.choice(RAC) # pick a species abundance at random
            if sp1_ab == 0:
                print 'you\'re model stick sucks. fix your bug'
                sys.exit()
                
            if sp1_ab == 1:
                continue # this is a control statement
                
            sp2_ab = randrange(1, sp1_ab) # pick a random number (abundance) between 1 and sp1_ab - 1, inclusive
            sp1_index = RAC.index(sp1_ab) # index in the RAC of the species we picked
            RAC[sp1_index] = sp1_ab - sp2_ab # decrease its abundance according to sp_ab
            
            RAC.append(sp2_ab)
            
        RAC_samples.append(RAC) # appending a list (i.e. an RAC) to another list
    
    return RAC_samples
    

N = 100 # total abundance
S = 4 # species richness
sample_size = 9

RAC_samples = simple_random_fraction(N, S, sample_size)
RAC_mean = [sum(x)/len(x) for x in itertools.izip(*RAC_samples)] #find mean for the lists in lists


RAC_hist = plt.hist(RAC_mean) #attempt to plot as histogram (not coming out right)
plt.title("RAC_Mean")
plt.show(RAC_hist)


print RAC_samples
print RAC_mean
