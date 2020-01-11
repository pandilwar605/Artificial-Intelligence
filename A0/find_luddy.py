#!/usr/local/bin/python3
#
# find_luddy.py : a simple maze solver
#
# Submitted by : [Sanket Pandilwar spandilw@iu.edu]
#
# Based on skeleton code by Z. Kachwala, 2019
#

import sys

# Parse the map from a given filename
def parse_map(filename):
    with open(filename, "r") as f:
        return [[char for char in line] for line in f.read().split("\n")]

# Check if a row,col index pair is on the map
def valid_index(pos, n, m):
    return 0 <= pos[0] < n  and 0 <= pos[1] < m

# Find the possible moves from position (row, col)
def moves(map, row, col, direction):
    moves=((row+1,col,direction+'S'), (row-1,col,direction+'N'), (row,col-1,direction+'W'), (row,col+1,direction+'E'))
    # Return only moves that are within the board and legal (i.e. on the sidewalk ".")
    return [move for move in moves if valid_index(move, len(map), len(map[0])) and (map[move[0]][move[1]] in ".@" )]

# Perform search on the map
def search1(IUB_map):
    # Find my start position
    you_loc=[(row_i,col_i) for col_i in range(len(IUB_map[0])) for row_i in range(len(IUB_map)) if IUB_map[row_i][col_i]=="#"][0]
    fringe=[(you_loc[0],you_loc[1],0,'')]
    '''
    Got the idea for using visited 2-d matrix to keep track of visited location from geeksforgeeks, from below link
    https://www.geeksforgeeks.org/breadth-first-search-or-bfs-for-a-graph/
    '''
    visited = [[0] * len(IUB_map[0]) for i in range(len(IUB_map))]
    '''Idea for initializing the 2-d array is taken from following website:(to avoid copying of reference)
        https://snakify.org/en/lessons/two_dimensional_lists_arrays/
    In this case each element is created independently from the others. The list [0] *
    m is n times consructed as the new one, and no copying of references occurs.'''

    for i in range(len(visited)):
        for j in range(len(visited[0])):
            visited[i][j]=False
    visited[you_loc[0]][you_loc[1]]=True
    while fringe:
        (row,col,curr_dist,direction)=fringe.pop(0)
        
        if IUB_map[row][col]=="@":
            return str(curr_dist)+' '+direction
        
        for move in moves(IUB_map,row,col,direction):
            if visited[move[0]][move[1]]==False:
                fringe.append((move[0],move[1], curr_dist + 1,move[2]))
                visited[move[0]][move[1]]=True
    return 'Inf'

# Main Function
if __name__ == "__main__":
    IUB_map=parse_map(sys.argv[1])
    print("Shhhh... quiet while I navigate!")
    solution = search1(IUB_map)
    print("Here's the solution I found:")
    print(solution)