#!/usr/local/bin/python3
# CSCI B551 Fall 2019
#
# Authors: Sanket Pandilwar (spandilw), Anuj Godase (abgodase), Amogh Batwal (abatwal)
#
# based on skeleton code by D. Crandall, 11/2019
#
# ./break_code.py : attack encryption
#

from __future__ import division
import random
import math
import string
import copy 
import sys
import encode
import numpy as np
import time

# put your code here!

#This function is to calculate probabilities of transitioning from one letter to another. eg., prob. of 1 a->p, t->z, etc
def transition_probability_distribution(corpus):
    
    chars = string.ascii_lowercase+" "
    transition_dict= {char:{} for char in chars}
    #Initially setting uniform probabilities for each letter
    for char in chars:
        for char2 in chars:
            transition_dict[char][char2]=1
            
    
    #Counting the occurence of letter to letter transition
    for i in range(1,len(corpus)):
        first_char=corpus[i-1]
        second_char=corpus[i]
        transition_dict[first_char][second_char]+=1
        
#    normalizing transition probabilities
    for k,v in transition_dict.items():
#        print(type(k), type(v))
        total=sum(v.values())
        for temp in v.keys():
            v[temp] = v[temp] / total
    
#   returning transition probability dictionary
    return transition_dict


#This function calculates initial probability distribution i.e probability of 1st letter of every word
def initial_probability_distribuition(corpus):
    chars = string.ascii_lowercase+" "
    initial={char:0 for char in chars}
    words=corpus.split()
    
    for word in words:
        initial[word[0]]+=1

    total=sum(initial.values())
    for temp in initial.keys():
        initial[temp] = initial[temp] / total

    return initial
    
#This function calculates log probabilities of document 
def log_probability_of_document(string,transition,initial):
    prob_of_document=0
#    calculating probability of each word 
    for word in string:
        prob_of_word=0
        if(len(word)<1):#In case there is empty list element e.g: ''
            continue        
        if(len(word)==1):#If there is only one letter in a word
            prob_of_word=math.log(initial.get(word[0]))
        else:
            prob_of_word=math.log(initial[word[0]])
            for i in range(1,len(word)): 
                if (transition[word[i-1]][word[i]])>0:                           
                    prob_of_word+=math.log(transition[word[i-1]][word[i]])
        prob_of_document+=prob_of_word
        
    return prob_of_document
   
#This function odifies replace encryption table by changing/swapping two of the letters from old table
def modify_replace(replace_table):
    letters = list(string.ascii_lowercase)
    random.shuffle(letters)
    first_letter=random.choice(letters)
    second_letter=random.choice(letters)
    rp=copy.deepcopy(replace_table)
    first_value=rp[first_letter]
    second_value=rp[second_letter]
    rp[first_letter]=second_value
    rp[second_letter]=first_value
    
    return rp
    
#This function odifies rearrangement encryption table by swapping two of the indices from old table
def modify_rearrangement(rearrangement_table):
    rand_ind=list(range(0,4))
    first_index=random.choice(rand_ind)
    second_index=random.choice(rand_ind)
    rt=copy.deepcopy(rearrangement_table)
    first_value=rt[first_index]
    second_value=rt[second_index]
    rt[first_index]=second_value
    rt[second_index]=first_value
    
    return rt

#This function modifies both the encryption tables    
def modify_encryption():    
    letters=list(range(ord('a'), ord('z')+1))
    random.shuffle(letters)
    replace_table = dict(zip(map(chr, range(ord('a'), ord('z')+1)), map(chr, letters)))
    rearrange_table = list(range(0,4))
    random.shuffle(rearrange_table)
    
    return replace_table,rearrange_table

#This function implements metropolis hasting algorithm to give proper decrypted document (hopefully!!!)
def break_code(string, corpus):
    transition=transition_probability_distribution(corpus)
    initial=initial_probability_distribuition(corpus)
    no_of_iterations=20000 # how many times sampling will be done to get better decrypted document
    
    
    old_replace_table,old_rearrange_table=modify_encryption() #Stores initial encryption tables    
    T_guess=encode.encode(string,old_replace_table,old_rearrange_table) #encoding
    T_prob=log_probability_of_document(T_guess.split(" "),transition,initial) # returns prob for guess with given encryption
    
    new_replace_table=copy.deepcopy(old_replace_table) #depcopy used to copy table in new table
    new_rearrange_table=copy.deepcopy(old_rearrange_table)
    while(no_of_iterations!=0):
        old_rearrange_table=copy.deepcopy(new_rearrange_table)
        old_replace_table=copy.deepcopy(new_replace_table)
        flag=random.randint(0,1)#generate random number among 0 and 1 to modify one of the two encryption tables
        if(flag == 0):
            new_replace_table=modify_replace(old_replace_table)    
        else:
            new_rearrange_table=modify_rearrangement(old_rearrange_table)
        
        
        T_hat=encode.encode(string,new_replace_table,new_rearrange_table) #encoding with modified encryption tables
        T_hat_prob=log_probability_of_document(T_hat.split(" "),transition,initial) # returns prob for guess with given encryption
        
        if(T_hat_prob > T_prob): # new guess is better than old
            T_prob=T_hat_prob      
        else: # new guess is not better than old
            if(np.random.binomial(1,np.exp(T_hat_prob-T_prob)) == 0 ): 
                if flag==1: #changing one of the two encryption tables
                    new_rearrange_table=copy.deepcopy(old_rearrange_table)
                else:
                    new_replace_table=copy.deepcopy(old_replace_table)
            else:
                T_prob=T_hat_prob
        no_of_iterations-=1
          
#    print(math.exp(T_hat_prob),math.exp(T_prob))
    return encode.encode(string,new_replace_table,new_rearrange_table)


if __name__== "__main__":
    if(len(sys.argv) != 4):
        raise Exception("usage: ./break_code.py coded-file corpus output-file")

    encoded = encode.read_clean_file(sys.argv[1])
    corpus = encode.read_clean_file(sys.argv[2])
    decoded = break_code(encoded, corpus)

    with open(sys.argv[3], "w") as file:
        print(decoded, file=file) 

