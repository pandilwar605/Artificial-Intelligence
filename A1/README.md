# Report

## Part 1: The Luddy Puzzle

### Implementation
We have employed the code using A* search algorithm with heuristic. There are lot of heuristics available to solve puzzle problems of this sort like Manhattan distance, number of misplaced tiles from goal, etc. The state space consists of all the explored states of the board during the heuristic search. The successor function consists of all the valid moves which are possible from the current board state as per the board variant. The edge weights are all one since no move is weighted in the process. The goal state is the board position consisting of numbers 1-15(from first position) in order and 0 in the last position. We have used Manhattan distance due to its efficiency and ease to code. We have also implemented Misplaced tiles heuristic in the same code. The function on line 105 needs to be replaced with the function name- ‘calculate_misplaced_tiles’ to change the heuristic. There is very minute difference in output between the two methods. Misplaced tile heuristic is admissible because it is clear that any tile that is out of place must be moved at least once, whereas Manhattan distance is admissible because all any move can do is move one tile one step closer to the goal. Thus, neither of these overestimates the true solution cost. Also, permutation inversion is implemented to check whether the board is solvable in the first place.

### Search Algorithm working
Manhattan distance calculates the City-block distance/Manhattan distance of each tile from its position in the current board position to its ideal position in the standard board. The cost function (known as f(s)) adds 1 each time (known as path cost) it explored one state corresponding to a chosen state to the Manhattan distance (known as h(s)). The minimum cost function is chosen and explored further until a solution state is reached.

### Problems faced
We had a hard time figuring out how to work with circular moves because of its special possible moves. Due to 3 variants, we had to change every function to work as per the variant entered by user. The design decision taken by us assumes that there is no extra character at the end of board state (after the last number on board).

## Part 2: Road trip!

### Implementation
We have implemented A* algorithm with heuristic. In this the heuristic adapts to the input given by the user and changes its value depending on user selected feature of importance which are 'segments', 'time', 'distance' and 'mpg'. 
Heuristic calculates following 
  1. haversine distance between city to be explored and goal city
  2. difference of angle between current city and goal city and city to be explored and goal city  
  3. base heuristic i.e one from segments, distance, time and mpg

The final cost of heuristic is calculated by taking weighted sum of above 3 factors.

##### Why such heuristic choice
Using base heuristic, we can find the optimal solution however, number of states it has to explore results in high amount of time to get solution. To improve this, we added haversine distance. This helps selecting the city which is close to the goal city. To improve more on this, we decided to add another variable of direction which is calculated by calculating slope between 1) current city and next city to be explored and 2) current city and goal city. Slope is calculated by using coordinates of the cities in context. Finding the slope helps choose optimal direction.

##### gps calculations
As the gps file does not have co ordinates for all the cities. I calculated approximated gps values by taking weighted average of connected cities. Weight for connected city was the distance between the cities.

##### Improvements

The implementation could be improved by storing heuristic cost for each connected city. So next time a particular fringe item is to be explored, we do not need to recalculate all the values again.
  
## Part 3: Choosing a team

### Implementation
We have employed the code using standard branch and bound methodology. This part can be solved using various approaches like dynamic programming or brute force at the least. The downsides of dynamic programming is, it doesn't work well with floating point values of rates or skills or budget. On the other hand, brute force approach is pretty simple approach and doesn't use any search techniques used in the coursework. The drawback of brute force is its high time complexity, as the no of people increases, complexity also increases. Hence, we didn't use the mentioned algorithms in the code. Branch and bound is a great all-round algorithm which works given any type of variable (integer/ float/ double). The start state is the first element after arranging the robots in decreasing order of (skill/rate) ratio. The successor function is any node whose bound is greater than maximum skill. The state space consists of all the comibnation of robot teams. The goal state is the team consisting of the highest skill and using the provided budget to the optimized value.

### Search Algorithm working

The specific type of branch and bound used by us is BFS branch and bound. For each node, if the current rate is less than the budget and current skill is greater than maximum skill, then we are updating the maximum skill. Similiarly, if the upper bound is greater, we are updating the maximum skill and pushing that node to the queue for further traversal. This process is repeated for each node which will compute the skill of every child i.e we are exploring all the nodes stored in the queue. 

### Problems faced

We faced plenty of issues when we first tried deploying the code using dynamic programming. Then, we tried brute force which wasn't much satisfying. Finally, we decided to go with Branch and Bound which provides absolute solution. No assumptions are made.

### Previous(discarded) approach for part 3

We used dynamic programming for such kind of optimization problems (known as knapsack problem). First, a table is created and maintained throughout the execution which keeps filling as per the working on the algorithm and provides the most efficient combination at the end of the table. The table is filled with the robot rate and skill as and when it is considered w.r.t. budget. When the table is generated, the efficient robot combination is tracked by parsing through the table and the output is provided. The state space consists of all the explored team combinations which are possible until the budget is reached. The successor function is the team which is chosen until the moment as per the remaining budget and maximum skill.  There are two approaches when a robot is available- either you choose the robot or you don’t choose the robot. According to each condition, the maximum value of the subset corresponding to each approach is chosen and processed in the form of a tree. The two values are: 1. Maximum value obtained by n-1 robot and B budget (excluding nth robot) 2. Value of nth robot plus maximum value obtained by n-1 robots and B minus budget of the nth robot (including nth robot). If rate of nth robot is greater than B, then the nth robot cannot be included and case 1 is the only possibility.
