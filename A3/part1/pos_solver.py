###################################
# CS B551 Fall 2019, Assignment #3
#
# Your names and user ids: Anuj Godase (abgodase), Sanket Pandilwar (spandilw), Amogh Batwal (abatwal)
#
# (Based on skeleton code by D. Crandall)
#


import random
import math
import sys
import numpy as np
import operator

# We've set up a suggested code structure, but feel free to change it. Just
# make sure your code still works with the label.py and pos_scorer.py code
# that we've supplied.

class Solver:
    # Calculate the log of the posterior probability of a given sentence
    #  with a given part-of-speech labeling. Right now just returns -999 -- fix this!
    def posterior(self, model, sentence, label):
        if model == "Simple":
            return self.simplified_posterior
        elif model == "Complex":
            return self.gibbs_posterior
#            return -999
        elif model == "HMM":
            return self.viterbi_posterior
        else:
            print("Unknown algo!")

    # Do the training!
    #
    def train(self, data):
        # Calculating the pos dictionry using train data.
        ## Looks like {word1 :{pos1:count of pos1, pos2: count of pos2}, word2:........}
        
        self.pos_dict=dict()
        self.pos_list=['adj','adv','adp','conj','det','noun','num','pron','prt','verb','x','.']
        for train in data:
            for i in range(len(train[0])):
                word=train[0][i]
                pos=train[1][i]
                if(word not in self.pos_dict):
                    self.pos_dict[word]={pos:0 for pos in self.pos_list}
                self.pos_dict[word][pos] += 1   
        pass
    
    def probability_distribution(self, train_data):
        self.transition_prob={pos:{} for pos in self.pos_list} # Empty dictionary of dictionary for pos transitions
        self.initial_prob=dict()
        self.emission_prob=dict()
        self.viterbi_initial=dict()
        
        ## Calculated transition probability i.e no. of times posx followed posy
        ## looks like {pos1:{pos2: count of such times, pos3: count of such time}, pos2:.......}        
        # making an empty dictionary for every transition possible i.e. 12*12
        for pos1 in self.pos_list:
            self.initial_prob[pos1]=0
            for pos2 in self.pos_list:
                self.transition_prob[pos1][pos2]=0
        
        for word in self.pos_dict:
            self.viterbi_initial[word]={pos:0 for pos in self.pos_list}
        
        for i in range(0,len(train_data)): # no. of words
            for j in range(0,len(train_data[i][1]) - 1): # range of no. of pos or no. of words (both are same length)                
                if (j==0):
                    if(train_data[i][0][j] in self.viterbi_initial):
                        self.viterbi_initial[train_data[i][0][j]][train_data[i][1][j]]+=1
                    self.initial_prob[train_data[i][1][j]]+=1  # increment the pos count as per occurence in training data 
                j = j + 1 # incrementing j for sake for making transition matrix
                # increment the value of transiiton from one pos to another
                self.transition_prob[train_data[i][1][j-1]][train_data[i][1][j]]+=1
                j = j - 1 # again bringing j to original value of loop

        for i in self.viterbi_initial:
            total=sum(list(self.viterbi_initial[i].values()))
            for j in self.viterbi_initial[i]:
                if(total==0):
                    continue
                else:
                    self.viterbi_initial[i][j]=self.viterbi_initial[i][j]/total
                    
        # initial probability calculation
        total = sum(self.initial_prob.values()) # total count of pos in training data
        for k in self.initial_prob.keys():
            self.initial_prob[k]=self.initial_prob[k]/total
        
#        normalizing transition probability dictionary
        for k,v in self.transition_prob.items():
            total=sum(v.values())  
            for temp in v.keys():
                if(total==0):
                    v[temp]=0
                else:
                    v[temp]=v[temp]/total
#        Emission probability
        self.count_pos={pos:0 for pos in self.pos_list} # initializing a pos dictionary with 0 value for each pos
        
        for x in self.pos_dict:
            self.emission_prob[x]={}
            for pos in self.pos_list:
                self.emission_prob[x][pos]=0  # associating the 12 pos for every word in train data
            
            for y in self.pos_dict[x]:
                self.count_pos[y]+=self.pos_dict[x][y]
                self.emission_prob[x][y]+=self.pos_dict[x][y]


#   Normalizing emission probability dictionaries        
        for x in self.emission_prob:
            for y in self.emission_prob[x]:
                self.emission_prob[x][y]=self.emission_prob[x][y] / self.count_pos[y]
        
        self.pos_normalized=[]
        total=sum(list(self.count_pos.values()))
        for i in self.count_pos:
            self.pos_normalized.append(self.count_pos[i]/total)
        pass
    
    
    # Functions for each algorithm. Right now this just returns nouns -- fix this!
    #
    def simplified(self, sentence):
        posterior_simplified=[]
        simplified_dict = []
        for i in range(len(sentence)):
            if(sentence[i] not in self.pos_dict):  # check if word is not in trained data words
                x = "noun" # if not, assign noun (bcoz its most common)
#                x=random.choice(self.pos_list) # if not, assign random pos 
                simplified_dict.append(x)
                posterior_simplified.append(1)
            else:
                x=max(self.pos_dict[sentence[i]], key=self.pos_dict[sentence[i]].get) # assign max pos value for that word
                simplified_dict.append(x)
                posterior_simplified.append(self.pos_dict[sentence[i]][x] / sum(self.pos_dict[sentence[i]].values()))

        self.simplified_posterior=np.log(np.prod(posterior_simplified))
        
        return simplified_dict # returning the predicted pos for that sentence

#Gibb's Sampling 
    def complex_mcmc(self, sentence):
        initial_value=['noun'] * (len(sentence))
        sampled_value_list=[] #stores probabilities calculated for each pos at each iterations
        samples=200
        posterior_gibbs=[]
        for sample in range(samples): #samples
            for i in range(len(sentence)): #iterate over words
                gibbs={} #to store all the pos probabilities calculated for each word
                for pos in self.pos_list:  #iterate for all the pos
                    initial_value[i] = pos
                    current_word=sentence[i]
                    prob=1
                    if(current_word not in self.emission_prob):
                        prob= prob * 0.000000001 #assigning default very low probability
                    else:                        
                        prob= prob * self.emission_prob[current_word][pos]
                    
                    if(i==0): #if it is first word of sentence
                        prob= prob * self.initial_prob[pos] #assigning initial probability
                    else: #else assigning transition probability
                        prob = prob * self.transition_prob[initial_value[i - 1]][pos]
                    gibbs[pos]=prob
                
                if(sample==samples-1):
                    posterior_gibbs.append(max(list(gibbs.values())))
                distribution=sum(gibbs.values())
                if distribution != 0: #normalizing all the probabilities
                    for k in gibbs.keys():
                        gibbs[k] = float(gibbs[k] / distribution)
                else:
                    distribution['noun'] = 1
                random_prob = random.random() #randomly generating a number to compare with probability
                pos_tag = 'noun'
                for pos_key,prob_value in gibbs.items():
                    if prob_value > random_prob:
                        pos_tag = pos_key
                        break
                    else:
                        pos_tag = 'noun'
                initial_value[i] = pos_tag
            sampled_value_list.append(initial_value)
        
        self.gibbs_posterior=np.log(np.prod(posterior_gibbs))
        gibbs_output = []  # stores a list of predicted pos output for each word
        count_of_words_for_pos = {} # stores word count for each pos
        for initial_value in sampled_value_list:
            for i in range(len(initial_value)):
                if i not in count_of_words_for_pos.keys():
                    count_of_words_for_pos[i] = {}
                if initial_value[i] not in count_of_words_for_pos[i].keys():
                    count_of_words_for_pos[i][initial_value[i]] = 0
                count_of_words_for_pos[i][initial_value[i]] += 1
        for pos_key in count_of_words_for_pos.keys():
            ''' following line of code to get key for max val is taken from https://stackoverflow.com/questions/268272/getting-key-with-maximum-value-in-dictionary'''
            gibbs_output.append(max(count_of_words_for_pos[pos_key].items(), key=operator.itemgetter(1))[0])
        
        return gibbs_output
            
# =============================================================================
# #Previous implementation of gibbs sampling which gave lesser sentence accuracy    
#     def extra_complex_mcmc(self, sentence): #Implementation of gibbs sampling
#         initial_value=['noun'] * (len(sentence)) #initially keeping it noun since it usually has highest probabilities
#         sampled_value_list=[[]] # one list for each sample 
#         samples=200
#         posterior_gibbs=[]
#         for i in range(0,samples):#samples            
#             for word_index in range(0,len(sentence)): #iterate over words
#                 prob_list=[]
#                 prob_sum=0
#                 for pos_index in range(0,12): #iterate for all the pos
#                     pos_to_prev_pos=0
#                     next_pos_to_current_pos=1
#                     current_pos=self.pos_list[pos_index]
#                     current_word=sentence[word_index]
#                     
#                     if(word_index ==0): #if it is first word of sentence
#                         pos_to_prev_pos=self.initial_prob[current_pos] #assigning initial probability
#                     else:
#                         pos_to_prev_pos=self.transition_prob[current_pos][initial_value[word_index-1]] #current to prev transition prob
#                     
#                     
#                     if(current_word not in self.emission_prob):
#                         word_to_pos=0
#                     else:                        
#                         word_to_pos=self.emission_prob[current_word][current_pos]
#                     
#                     if pos_index < (len(sentence)-1):
#                         next_pos_to_current_pos = self.transition_prob[initial_value[pos_index+1]][current_pos]
#                     calculated_prob= pos_to_prev_pos * next_pos_to_current_pos *word_to_pos
#                     prob_sum+=calculated_prob
#                     prob_list.append(calculated_prob)
#                 
#                 temp_index=5 #temperoary keeping a noun index
#                 cummulative_sum=0
#                 random_uniform_prob=random.uniform(0.00, 1.00)
#                 for prob_index in range(0,len(prob_list)):
#                     if(prob_sum==0):
#                         prob_list[prob_index]=0
#                     else:
#                         prob_list[prob_index] = prob_list[prob_index] / prob_sum
#                     cummulative_sum+=prob_list[prob_index]
#                     prob_list[prob_index] = cummulative_sum #storing cummulative sum
#                     if(random_uniform_prob < prob_list[prob_index]): #checking if random uniform probaility is lesser than cummulative prob
#                         temp_index=prob_index
#                         if(i==samples-1):
#                             posterior_gibbs.append(prob_list[prob_index])
#                         break
#                 
#                 initial_value[word_index] = self.pos_list[temp_index]
#             sampled_value_list.append(initial_value)
#         self.gibbs_posterior=np.log(np.prod(posterior_gibbs))
# #        print(sampled_value_list[samples-1])
# #        return [ "noun" ] * len(sentence) 
# #        print(np.log(prob))
#         return sampled_value_list[samples-1]
# =============================================================================
 
#Viterbi Implementation       
    def hmm_viterbi(self, sentence):
        posterior_viterbi=[]
        word=sentence[0]
        initial_prob=[]
        
        if word not in self.viterbi_initial:
            initial_prob = list(self.initial_prob.values())
        else:
            initial_prob = list(self.emission_prob[word].values())    
        
        viterbi=[]
        vi=np.asarray(initial_prob).T
        viterbi.append(vi)
        posterior_viterbi.append(np.max(vi))
        for i in range(1,len(sentence)):
            word=sentence[i]
            if word not in self.emission_prob:
                emm_word=np.asarray(self.pos_normalized)
            else:
                emm_word=np.asarray(list(self.emission_prob[word].values()))
            prev_pos=self.pos_list[np.argmax(vi)]
            trans_word=np.asarray(list(self.transition_prob[prev_pos].values()))
            vj= emm_word * np.max(2*trans_word * vi)
            vi=vj
            posterior_viterbi.append(np.max(trans_word))
            viterbi.append(vj)
        
        viterbi=np.array(viterbi)
        
        posses = np.argmax(viterbi, axis = 1)  # Index of the predicted pos's
        hmm_output=[]
        
        for i in posses:
            hmm_output.append(self.pos_list[i])

        self.viterbi_posterior=np.log(np.prod(posterior_viterbi))            
        return hmm_output


    # This solve() method is called by label.py, so you should keep the interface the
    #  same, but you can change the code itself. 
    # It should return a list of part-of-speech labelings of the sentence, one
    #  part of speech per word.
    #
    def solve(self, model, sentence):
        if model == "Simple":
            return self.simplified(sentence)
        elif model == "Complex":
            return self.complex_mcmc(sentence)
        elif model == "HMM":
            return self.hmm_viterbi(sentence)
        else:
            print("Unknown algo!")

