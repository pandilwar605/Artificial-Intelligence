#!/usr/local/bin/python3
# solve_luddy.py : Sliding tile puzzle solver
#
# Code by: Amogh Batwal(abatwal), Anuj Godase(abgodase), Sanket Pandilwar(spandilw)
#
# Based on skeleton code by D. Crandall, September 2019
#
from queue import PriorityQueue

import sys

# Moves defined for all 3 variants
MOVES_original = { "R": (0, -1), "L": (0, 1), "D": (-1, 0), "U": (1,0) }
MOVES_luddy = { "A": (2, 1), "B": (2, -1), "C": (-2, 1), "D": (-2, -1), "E": (1, 2), "F": (1, -2), "G": (-1, 2), "H": (-1, -2)  }
MOVES_circular= { "R": (0, -1), "L": (0, 1), "D": (-1, 0), "U": (1,0) }

def rowcol2ind(row, col):
    return row*4 + col

def ind2rowcol(ind):
    return (int(ind/4), ind % 4)

def valid_index(row, col,variant):
    if variant=='circular':   # To make sure the row and column numbers remain between 0 & 3
        return 0 <= (row%4) <= 3 and 0 <= (col%4) <= 3
    else:    
        return 0 <= row <= 3 and 0 <= col <= 3

def swap_ind(list, ind1, ind2):    
    return list[0:ind1] + (list[ind2],) + list[ind1+1:ind2] + (list[ind1],) + list[ind2+1:]

def swap_tiles(state, row1, col1, row2, col2, variant):
    if variant=='circular':
        return swap_ind(state, *(sorted((rowcol2ind(row1,col1), rowcol2ind(row2%4,col2%4)))))
    else:
        return swap_ind(state, *(sorted((rowcol2ind(row1,col1), rowcol2ind(row2,col2)))))

def printable_board(row):
    return [ '%3d %3d %3d %3d'  % (row[j:(j+4)]) for j in range(0, 16, 4) ]

# Return a list of possible successor states
def successors(state,variant):
    (empty_row, empty_col) = ind2rowcol(state.index(0))
    # Passing the variant alongwith the valid moves so that the respective statements are executed
    return [ (swap_tiles(state, empty_row, empty_col, empty_row+i, empty_col+j,variant), c) \
             for (c, (i, j)) in (MOVES_original.items() if variant=='original' else (MOVES_luddy.items() if variant=='luddy' else MOVES_circular.items())) if valid_index(empty_row+i, empty_col+j,variant) ]

# Calculation of Manhattan distance from the goal state
def calculate_manhattan(succ,standard_board):
    h_cost=0
    for i in range(1,16):
        (row1, col1) = ind2rowcol(succ.index(i))
        (row2, col2) = ind2rowcol(standard_board.index(i))
        h_cost= h_cost + abs(row1-row2) + abs(col1-col2)   # Manhatten distance computation
    return h_cost

# Calculation of Misplaced tiles from goal state
def calculate_misplaced_tiles(succ,standard_board):
    no_of_tiles=0
    for i in range(1,16):
        (row1, col1) = ind2rowcol(succ.index(i))
        (row2, col2) = ind2rowcol(standard_board.index(i))
        if not (row1==row2 and col1==col2):  # Check of misplaced tiles
            no_of_tiles+=1
    return no_of_tiles    

# Check if we've reached the goal
def is_goal(state):
    return sorted(state[:-1]) == list(state[:-1]) and state[-1]==0
    
# The solver!
def solve(initial_board,variant):
    fringe = PriorityQueue()
    standard_board=(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0)
    
    visited=set()
    fringe.put((0,initial_board,"",0))
    if(variant=='original'):
        inversion=list(initial_board)
        (empty_row, empty_col) = ind2rowcol(initial_board.index(0))
        n=4 #4*4 puzzle board
        n_state=0
        inversion.remove(0)
        for tile_idx in range(0,len(inversion)):
            if(tile_idx < len(inversion)):
                for idx in range(tile_idx+1,len(inversion)):
                    if inversion[tile_idx]>inversion[idx]:
                        n_state+=1
        
        if (((n-empty_row)%2==0 and n_state%2==0) or ((n-empty_row)%2!=0 and n_state%2!=0)): 
            return 'Inf'

    visited.add(initial_board)
    while not fringe.empty():
        fringe_element = fringe.get()
        g=0
        g=fringe_element[3]+1
        (state,route_so_far)=(fringe_element[1],fringe_element[2])
        if is_goal(state):
            return(route_so_far)
        for (succ, move) in successors(state,variant): 
            if succ not in visited:
                visited.add(succ)
                if variant == 'luddy':                    
                    fringe.put((g+calculate_misplaced_tiles(succ,standard_board), succ, route_so_far + move, g))
                else:
                    fringe.put((g+calculate_manhattan(succ,standard_board), succ, route_so_far + move, g))
            
    return False

if __name__ == "__main__":
    if(len(sys.argv) != 3):
        raise(Exception("Error: expected 2 arguments"))
   
    start_state = [] 
    with open(sys.argv[1], 'r') as file:
        for line in file:
            start_state += [ int(i) for i in line.split() ]

#    if(sys.argv[2] != "original"):
#        raise(Exception("Error: only 'original' puzzle currently supported -- you need to implement the other two!"))

    if len(start_state) != 16:
        raise(Exception("Error: couldn't parse start state file"))

    print("Start state: \n" +"\n".join(printable_board(tuple(start_state))))

    print("Solving...")
    route = solve(tuple(start_state),sys.argv[2])
    if(route=='Inf'):
        print('Inf')
    else:
        print("Solution found in " + str(len(route)) + " moves:" + "\n" + route)
