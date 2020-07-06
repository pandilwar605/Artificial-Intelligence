# Part 1: Part-of-speech tagging

Using the train data, we created a dictionary which contained all the words with their pos and their counts. Emission, initial and transition probabilities are calculated using the training data. 
Emission probability is the probability of a word given its pos. Transition probability is the probability of a word occuring given previous word in the sequence. Initial probability is the probability of that word's pos' occuring as first word in the training data.

## 1. Simplified Bayes Net
In this section, we chose the maximum value of each POS as it occured in the training data for that word. We iterate through each word in the test data and get the corresponding words' maximum POS value in the training data. For posterior calculation, we multiply the probability of each word's POS prediction.
We got an accuracy of 47.5% for sentences and 93.95% for the words. 

## 2. HMM Viterbi
In this section, we use the emmission, initial and transition probabilities for the calculation of the viterbi parameter. For the first word in the sentence, we take the initial probability . For the rest fo the words, multiply the emission probability(probability of word given post, so it's a vector of 12 elements (12 POS)), transition probability(probability of the current word occuring given that we selected the previous word) and the probability of choosing the previous word in the sequence. 
We received an accuracy of 41.1% for the sentences and 92.63% for the words. 
We tried to increase the accuracy of sentences to 50%+ but could not do it. We could have improved our implementation of the posterior calculations which can lead to effective results.

## 3. Gibb's Sampling
Gibb's Sampling is one of the MCMC techniques which is used to generate samples from posterior distribution. In this part, we have used 200 samples. In each iteration, for each word, 12 pos probabilities will be calculated using emission,initial and transition probability distribution. Then we estimate the best labeling for each word by these generated samples and by checking for each word, which pos occured most often (can be retrieved from storing counts for pos and word while generating samples).
We received an accuracy of 37.45% for the sentences and 91.21% for the words. 
        
# Part 2: Code breaking

In this part, to decrypt a document we have used a metropolis hasting algorithm which is variant of MCMC Samling. In metropolis hasting algorithm, we produce samples from probability distribution. There are two encryption tables which can be used to decipher a document, rearrangement and replacement tables. We have used 20000 samples in this assignemnt. In each iteration, one of the two encryption tables are modified to decipher the document and calculating probabilities. Whichever(old and new) encryption tables have higher probabilities, they will be used in further iterations. 

# Part 3: Spam classification

#### Implementation
In this part we have implemented the famous naive bayes algorithm to classify spam and ham emails.
Following are the steps done in the final implementation of this code.
1) Preprocessing: In this part we use regex to remove spaces and puctuations.
2) Populating the model: Here we create 3 dictionaries which contain the spam and words with its occurences and third dictionary contains counts of total words.
3) Prediction: Here, as it was suggested in the assignment, We have calculated the contional probability using bayes law. To avoid underflow of numbers, we have implemented logarithemic version. While predicting we have set threshold of spam to ham ratio to 2 for predicting if its spam or not

#### Issues faced
When we first implemented first version, we were preprocessing the data and populating the dictionaries containing the spam and ham propabilities by iterating one by one on the words. This implementataion resulted in about 65% accuracy however time taken to execute the program was about 30-40 minutes.

To address this, we used regexes to preprocess the data. Now the code takes about 4-5 minutes to execute. 
However the accuracy has gone down due to the preprocessing includes some unnecessary words. 
This should ideally have been taken care by the naive bayes algorithm as these uncessary words should have lower probability
