#!/usr/local/bin/python3

"""
This is where you should write your AI code!

Authors: PLEASE ENTER YOUR NAMES AND USER ID'S HERE

Based on skeleton code by Abhilash Kuhikar, October 2019
"""

from logic_IJK import Game_IJK
import random
import math
from collections import Counter

# Suggests next move to be played by the current player given the current game
#
# inputs:
#     game : Current state of the game
#
# This function should analyze the current state of the game and determine the
# best move for the current player. It should then call "yield" on that move.

moves = ['U', 'D', 'L', 'R']

def utility(board):
    score = 0

    for row in board:
        for col in row:
            if col.isupper():
                score = score + (ord(col) - 65)

            if col.islower():
                score = score - (ord(col) - 96)

            # if col == ' ':
            #     score = score+1
    return score

def  utility2(board):
    #get all rows
    #   for every row, if even number of same letters add score per letter to left and right
    #get all columns
    #   for every row, if even number of same letters add score per letter to left and right
    score = 0
    for row in board:
        dictionary = Counter(row)
        for let in dictionary.keys():
            if dictionary[let]%2 == 0:
                score+=1

    transposed_board = [[
        [board[j][i] for j in range(len(board))] for i in range(len(board[0]))
    ]]

    for column in transposed_board:
        dictionary = Counter(row)
        for let in dictionary.keys():
            if dictionary[let]%2 == 0:
                score+=1

    return score


def utility3(board):
    score = 0
    # build on top of utility 2
    # even values on left add score to left, even values on right, add right
    # even values on up add score to up, even values on down, add down
    return score

def Min(move, game: Game_IJK, depth, alpha, beta):

    game = game.makeMove(move)

    depth = depth + 1
    board = game.getGame()

    if(depth == 6):
        return [utility(board), move]

    for m in moves:
        beta, move = min([beta, move], Max(move, game, depth, alpha, beta))
        if alpha > beta:
            return [beta, move]

    return [beta, move]

def Max(move, game: Game_IJK, depth, alpha, beta):

    game = game.makeMove(move)

    depth = depth + 1
    board = game.getGame()

    if(depth == 6):
        return [utility(board), move]

    for m in moves:
        alpha, move = max([alpha, move], Min(move, game, depth, alpha, beta))
        if alpha > beta:
            return [alpha, move]
    return [alpha, move]

def next_move(game: Game_IJK)-> None:

    '''board: list of list of strings -> current state of the game
       current_player: int -> player who will make the next move either ('+') or -'-')
       deterministic: bool -> either True or False, indicating whether the game is deterministic or not
    '''

    board = game.getGame()
    player = game.getCurrentPlayer()
    deterministic = game.getDeterministic()

    # You'll want to put in your fancy AI code here. For right now this just
    # returns a random move.

    depth = 0

    alpha = -math.inf
    beta = math.inf
    mv = ''
    to_be_done = ''

    unchanged_board = board

    for m in moves:
        alpha, mv = max([alpha,mv], Min(m, game, depth, alpha, beta))
        to_be_done = mv
    return to_be_done

    # yield random.choice(moves)
