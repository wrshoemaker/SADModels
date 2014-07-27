from __future__ import division
import sys                                            
import numpy as np
import math
import random
import matplotlib.pyplot as plt
import scipy.stats                                       
from random import randrange, randint, uniform, seed, choice



"""This script codes Broken Stick models for species abundance distribution.
    These are generally conceived as models for how species partition a niche
    dimension or shared and limited resource. -KL 
    
    Task: Nathan contribute one or two nice sentences. """
    
     
def SimBrokenStick(N, S, sample_size):
    
    """
    A function to generate random samples of the simultaneous Broken Stick Model
    of MacArthur 1957 or 1961. We need the actual citation.
        
    N  :  Total abundance, i.e., number of individuals
    S  :  Species richness, i.e., number of species
    sample_size  :  number of rank-abundance vectors to generate
    
    How this model works.  Create list of range of N, then make S - 1 random 
    divisions in range of N, repeat sample_size times. So, first we have to get
    our indices. Which you've figured out. Then, we can split a list of N 1's at
    those indices points. A few rules apply, e.g. 0 can't be one of the indices.
    Say the simultanesouly drawn indices are [2, 9, 5]. Here, simultaneous means
    those numbers were drawn without replacement, i.e., were not allowed to
    can't draw any number twice. Once you sort those numbers then you can...
    
    Hint: Let N = 15, S = 4, and SortedIndices = [2, 5, 9]
    So: oo|ooo|oooo|oooooo  = [2, 3, 4, 6] -> N = 15 and S = 4
    2-0 = 2  :  5-2 = 3  :  9-5 = 4  :  15-9 = 6
    
    """    

    
    RACs = []
    RAC = []
    
    while len(RACs) < sample_size:
        
        cuts = random.sample(range(N), S-1) # This is a time costly operation
                                            # We want something faster                       
        cuts.sort()
        RAC = [cuts[0]]
        
        sp_ab = float()
        cut = float()
        for i, cut in enumerate(cuts):    
            if i == 0:
                continue
            
            sp_ab = cut - cuts[i-1]
            RAC.append(sp_ab)
        
        RAC.append(N - cut) 
        RAC.sort(reverse = True)    
        RACs.append(RAC)
        
        
        for _list in RACs:
            if sum(RAC) !=N or len(RAC) != S:
                print 'Incorrect N and S: N=',sum(RAC),' S=', len(RAC)
                sys.exit()
                
    return RACs 
    
   
'''This script codes Tokeshi's Dominance Preemption Model
this code does not work well with small N or high S'''

def DomPreInt(N, S, sample_size): # Works only with positive integers
    sample = [] # A list of RACs
   
    while len(sample) != sample_size: # number of samples loop     
        RAC = [] #RAC is a list
        sp1 = randrange(int(N *.5), N) #Rand select from N to N(.5)
        ab1 = N - sp1
        RAC.extend([sp1, ab1]) 
        
        while len(RAC) < S:
            ab2 = RAC.pop()
            if ab2 < S - len(RAC):
                break
            sp2 = randrange(int(ab2*.5), ab2)
            RAC.extend([sp2, ab2-sp2])

        if len(RAC) == S and sum(RAC) == N:
            sample.append(RAC)
        #else:
            #print len(RAC), sum(RAC)
        
    return sample


def DomPreFloat(N, S, sample_size):#Works with decimal values
    sample = [] # A list of RACs
   
    for i in range(sample_size):     
        RAC = []
        sp1 = uniform((N *.5), N) 
        ab1 = N - sp1
        RAC.extend([sp1, ab1])
       
        
        while len(RAC) < S:
            ab2 = RAC.pop()
            sp2 = uniform((ab2*.5), ab2)
            RAC.extend([sp2, ab2-sp2])
            
    	sample.append(RAC)
        
    return sample
    
    
def SimLogNorm(N, S, sample_size):
    
    sample = []
    while len(sample) < sample_size:
        RAC = [0.75*N, 0.25*N]
        
        while len(RAC) < S:
            ind = randrange(len(RAC))
            v = RAC.pop(ind)
            v1, v2 = int(0.75 * v), v - int(0.75 * v) # forcing all abundance
                                                      # values to be integers
            
            if v1 < 1 or v2 < 1: break  # forcing smallest abundance to be 
                                        # greater than one
            RAC.extend([v1, v2])
        
        if len(RAC) == S and sum(RAC) == N:
            RAC.sort()
            RAC.reverse()
            sample.append(RAC)
            #print len(sample)
            
    return sample


'''This script codes the Pareto Model'''
def SimPareto(N, S, sample_size, integer=False):
    
    sample = []
    
    for i in range(sample_size): 
        
        
        RAC = [0.8*N, 0.2*N]
        
        while len(RAC) < S:
            ind = randrange(len(RAC))
            v = RAC.pop(ind)
            v1, v2 = [0.8 * v, v - 0.8 * v]
            RAC.extend([v1, v2])       
                        
        if integer == True:    
            if sum(RAC) !=N or len(RAC) != S:
                #print 'Incorrect N and S: N=',sum(RAC),' S=', len(RAC)
                sys.exit()
        elif integer == False:
            if len(RAC) != S:
                #print 'Incorrect S:', len(RAC)
                sys.exit()
        else: 
            #print 'Integer values need to be either \'False\' or \'True\''
            sys.exit()
       
        RAC.sort(reverse = True)
        sample.append(RAC)
    
    return sample
    
    
def Sample_SimpleRandomFraction(N, S, sample_size):
    
    """ 
    This function randomly and sequently splits N into two integers by
    starting with a vector where N is the only value, i.e. N, and then splitting
    N into two positive integers at random, [N] -> [x1, x2], where x1+x2 = N.
    The function then draws one of the integers at random from the new vector
    (having 2 values), and then splits the integer into two other integers. 
    At this point, the vector has three values [x1, x2, x3], where x1+x2+x3 = N.  
    This process keeps on until there are a number of integers equal to S.
    
    N  :  total abundance; number of individuals in the community
    S  :  species richness; number of species in the community
    sample_size  :  number of random rank-abundance vectors to generate    
    """
    
    sample = []
    for i in range(sample_size):
        RAC = [N]
        
        while len(RAC) < S:
                
            sp1_ab = choice(RAC) # pick a species (i.e. vector value) abundance at random
            if sp1_ab == 0:
                #print 'you\'re model has a bug'
                sys.exit()
                
            if sp1_ab == 1:
                continue # this is a control statement to prevent the program
                # from encountering an impossible conditions, i.e., dividing 1
                # at random into two positive integers
                
            sp2_ab = randrange(1, sp1_ab) # pick a random number (abundance) between 1 and sp1_ab - 1, inclusive
            sp1_index = RAC.index(sp1_ab) # index in the RAC of the species we picked
                
            RAC[sp1_index] = sp1_ab - sp2_ab # decrease its abundance according to sp_ab
            RAC.append(sp2_ab)
            
        RAC.sort(reverse = True)  #sorts RAC's in decending order to aid in graphing. 
        #Ken: Nice job. But it was in a loop that caused it to be repeated w/out need.
        
        sample.append(RAC) # appending a list (i.e. an RAC) to another list
        
    return sample
    
def DomFloat(N, S, sample_size): # Works only with positive integers
    sample = [] # A list of RACs
   
    while len(sample) != sample_size: # number of samples loop     
        RAC = [] #RAC is a list
        sp1 = uniform(0,  N*.5) #Rand select from N to N(.5)
        ab1 = N - sp1
        RAC.extend([sp1, ab1]) 
        
        while len(RAC) < S:
            ab2 = RAC.pop()
            sp2 = uniform(0, ab2 *.5)
            RAC.extend([sp2, ab2-sp2])

        if len(RAC) == S and int(round(sum(RAC))) == N:
            RAC.sort(reverse = True)
            sample.append(RAC)
        #else:
            #print len(RAC), sum(RAC)
        
    return sample

    
