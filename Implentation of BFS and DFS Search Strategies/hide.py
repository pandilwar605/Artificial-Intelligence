#!/usr/local/bin/python3
#
# hide.py : a simple friend-hider
#
# Submitted by : [Sanket Pandilwar spandilw@iu.edu]
#
# Based on skeleton code by D. Crandall and Z. Kachwala, 2019
#
# The problem to be solved is this:
# Given a campus map, find a placement of F friends so that no two can find one another.
#

import sys

# Parse the map from a given filename
def parse_map(filename):
	with open(filename, "r") as f:
		return [[char for char in line] for line in f.read().split("\n")]

# Count total # of friends on board
def count_friends(board):
    return sum([ row.count('F') for row in board ] )

# Return a string with the board rendered in a human-friendly format
def printable_board(board):
    return "\n".join([ "".join(row) for row in board])

# Add a friend to the board at the given position, and return a new board (doesn't change original)
def add_friend(board, row, col):
    return board[0:row] + [board[row][0:col] + ['F',] + board[row][col+1:]] + board[row+1:]

# Get list of successors of given board state
def successors(board):
    return [ add_friend(board, r, c) for r in range(0, len(board)) for c in range(0,len(board[0])) if (board[r][c] == '.' and check_config(board,r,c)==True)]


def check_config(board,row,col): #Before adding a friend, check if any friend is in sight
    each_loc=[row,col]
    row_list=(board[each_loc[0]])# will return row at each_loc[0] code referred from:'''https://stackoverflow.com/questions/36436425/slicing-list-of-lists-in-python'''
    for i in range(len(board[0])):#checking other F's in same row
        if(i!=each_loc[1]) and (row_list[i]=='F'):
            if(i>each_loc[1]):
                if '&' not in row_list[each_loc[1]:i]:
                    return False
            else:
                if '&' not in row_list[i:each_loc[1]]:
                    return False
                
    inverted_board=[[x[idx] for x in board] for idx in range(len(board[0]))] #'''https://stackoverflow.com/questions/21444338/transpose-nested-list-in-python/21444360#21444360'''
    col_list=(inverted_board[each_loc[1]])# will return row at each_loc[1]
    for i in range(len(inverted_board[0])):#checking other F's in same column by transposing board
        if(i!=each_loc[0]) and (col_list[i]=='F'):
            if(i>each_loc[0]):
                if '&' not in col_list[each_loc[0]:i]:
                    return False
            else:
                if '&' not in col_list[i:each_loc[0]]:
                    return False
                
    return True

# check if board is a goal state
def is_goal(board):               
    return count_friends(board) == K 

# Solve n-rooks!
def solve(initial_board):
    fringe = [initial_board]
    visited=[]
    while len(fringe) > 0:
        current_state=fringe.pop()
        visited.append(current_state)
        if is_goal(current_state):
            return(current_state)
        for s in successors(current_state):
            if(s not in visited):
                visited.append(s)
                fringe.append(s)
    return False

# Main Function
if __name__ == "__main__":
    IUB_map=parse_map(sys.argv[1])
    # This is K, the number of friends
    K = int(sys.argv[2])
    print ("Starting from initial board:\n" + printable_board(IUB_map) + "\n\nLooking for solution...\n")
    solution = solve(IUB_map)
    print ("Here's what we found:")
    print (printable_board(solution) if solution else "None")
