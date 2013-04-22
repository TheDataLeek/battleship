#!/usr/bin/env python

'''
Battleship! The Game

Ship Classes:
    aircraft
    battleship
    submarine
    destroyer
    patrol
'''

import sys
import os
import numpy
import argparse

import pygame

pos_dict = {'A':0,
            'B':1,
            'C':2,
            'D':3,
            'E':4,
            'F':5,
            'G':6,
            'H':7,
            'I':8,
            'J':9}

players = []

def main():
    pygame.init()

    args = get_args()
#    print args

#    clear_screen()

    if args.players != 2:
        ans = raw_input('Error, AI not enabled or invalid player count... Continue? (y/n) ')
        if ans.lower() == 'y':
            args.players = 2
        else:
            sys.exit(0)

    for number in range(args.players):
        new_player = Player(args.gridsize)
        players.append(new_player)

    switch(1)

def switch(player_num):
    '''
    Clears screen and holds for player (player_num)
    '''
#    clear_screen()
    text = 'PLAYER %i PLEASE CONTINUE' %player_num
    raw_input(text)

def clear_screen():
    '''
    Clears the screen and readies for the next state
    '''
    os.system('clear')

def gen_grid(size):
    '''
    Creates a 10x10 grid and returns
    '''
    a_grid = []
    for row in range(size):
        row = []
        for number in range(size):
            row.append(0)
        a_grid.append(row)
    grid = numpy.array(a_grid)
    return grid

def get_args():
    '''
    Gets user input from command line
    '''
    parser = argparse.ArgumentParser(description='Battleship, The Game!')
    parser.add_argument('-p', '--players', type=int, default=2, help='How many players')
    parser.add_argument('-g', '--gridsize', type=int, default=10, help='Grid Size')
    args = parser.parse_args()
    return args

class Player:
    '''
    Player Class
    Contains Shiplist and Grid
    '''

    def __init__(self, gridsize):
        '''
        Initializes a Player
        '''
        self.grid     = gen_grid(gridsize)
        self.shiplist = []

    def shoot(self, pid, coord):
        '''
        Shoot at specified player at specified coordinates
        '''
        target = players[pid]
        for item in target.shiplist:
            result = item.register(coord)
            if result == True:
                print 'Hit!'
            elif result == False:
                print 'Miss!'
            else:
                print result

if __name__=="__main__":
    sys.exit(main())
