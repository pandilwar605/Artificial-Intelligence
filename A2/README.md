# Report

## Part 1: IJK

### We have implemented this game using minimax with alpha-beta pruning and looking 6 steps ahead (has a depth of 6) of the current position of the board. It backs up the value which is going to increase the chances of winning for that player. We tried implementing 3 heuristics for our program.

### The first heuristic is simply the subtraction of the no. of tiles of player 1 and no. of tiles of player 2. The board which has this value highest is chosen and backed up. This one is used in the running and submitted code.

### The second heuristic is: if 2 same alphabets having the same case lie on a row or a column, they add up to the final score. So, there needs to even a pair of alphabets. Then only score gets added to that particular board configuration. E.g.: if one of the rows contains ‘aa’ as well as ‘AA’, then that row gets a score of 2. The same goes for a situation in a column. Finally, all these scores add to the board score. 

### We had the third heuristic in mind but due to lack of time, we couldn’t implement it. This heuristic is built on top of heuristic 2 where instead of giving scores based on the same pairing, we give score even if two different case alphabets are beside each other. E.g.: if one of the rows contains ‘a’ as well as ‘A’, then that row gets a score of 1. The same goes for a situation in a column. Finally, all these scores add to the board score.

### We ran around 12 trials for choosing the efficient heuristic for both det and nondet. In the trials, our first heuristic won 9 games, second heuristic won 2 and one ended in a tie. Hence, we went ahead with the first heuristic.

## Part 2: Horizon Finding
### In the first part of the code, the Bayes nets simply picks up the maximum value from the edge strength map for that column. This leads to very poor results of the output. But, that is expected from a Bayes net where there is no intelligence used in selecting the ridge points.

### In the second part of the code, we are asked to implement Viterbi algorithm since it’s a good method to find the most likely sequence of the hidden variables (which are basically the points lying on the ridge) on the basis of transition probabilities (data point lying on the ridge in current column given the data point on previous column), the probability of the point lying at current coordinate of the map and the emission probability (probability of data point lying in the current column given the edge strength on that column). We have considered the first column as the normalized values of the edge strength in that column. After that, the Viterbi formula is used to calculate the probability. This process is repeated until it reaches the last column. For transition probability, we are only exploring 10% of the rows (close vicinity) which lie in the next column from the current maximum data point (calculated from Viterbi). This reduces our unnecessary search for ridge points far from the current data point as they definitely would not lie that far. The downside of this approach is it fails to detect horizon when the edge strength of the mountain is low compared to the other strong points which have a high gradient. This is because the initial point in the first column is itself the point which has the highest gradient. This can be resolved if the starting point is chosen appropriately. Also, few points have emission which dominate over better ridge contestants.

### In the third part of the code, given the human input coordinates which lie on the ridge, we started our exploration of the ridge forward and backward from that data point. The human coordinate gets initial state distribution probability as 1 since it is definite to lie on a ridge. The same logic is used as Viterbi in part 2. The human input provides a lot of improvement as compared to the second part. It acts as a helping hand to the search even to the faint mountain images. 
