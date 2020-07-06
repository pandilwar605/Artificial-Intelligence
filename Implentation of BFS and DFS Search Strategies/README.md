# Assignment a0 Part-I

Initial State = {your location}

Goal State = {Location of @}

State Space = {(x0,y0),(x1,y0),......(xm,yn)} - {the locations at '&'} where m is no. of rows and n is no. of columns in map file

Successfor Function = move('S' || 'N' || 'W' || 'E')

Cost Function = 1 (Constant)

## My line of thinking for the first part:
After running the program as it is for the first time, I got to know, 
it was going in an infinite loop because it kept going back and forth to the same locations. 
So, I replaced stack with queue and created one m * n 2-d array to keep track of visited nodes. 
If you are dealing with the search problem where the cost of each node is equal then, 
BFS would be the best choice (my understanding) because its complete and optimal. 
I have implemented this part using BFS. Programatically, when I am visiting successor from the current state, 
I am just appending current states path to successor state so that we know from where did we traverse this state later 
which will help us in getting a path.


# Assignment a0 Part-II

Initial State = {Map file with no friends added}

Goal State = {Board state where all friends are placed properly || No solution}

State Space = {Possible number of board states}

Successor Function = Checking constraint and adding i'th friend on board. 

Cost Function = There is no cost associated with it since we are checking the board state and we are not using any heuristics.

## Working of the second part

For this part, First I initialized fringe with map file as an initial state. 
Before adding any friend to the current_state (with the help of successor function), constraint check is done so that no two friends can be on the same column/row unless there is a building between them. 
This is iterated for all the board states and will stop when the fringe is empty.
To avoid visiting duplicate states, the list is maintained which will check whether the state has been previously visited or not. 
If not visited, it will add it to list after visiting. 



