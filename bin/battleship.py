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
import random

try:
    import pygame
    from pygame import Color, Rect, Surface

    import numpy
    import argparse
except ImportError:
    print 'Error, Missing Libraries'
    sys.exit(0)

players = []

def main():
    args = get_args()

    clear_screen()

    if args.players != 2:
        ans = raw_input('Error, AI not enabled or invalid player count... Continue? (y/n) ')
        if ans.lower() == 'y':
            args.players = 2
        else:
            sys.exit(0)

    for number in range(args.players):
        new_player = Player(args.gridsize, number)
        players.append(new_player)

    initialize_game(args)

    game_list = []
    for item in players:
        game_list.append(item)

    Screen()

def initialize_game(args):
    '''
    Sets up the board for the player
    '''
    shipsizes = [5, 4, 3, 3, 2]
    for cp in players:
#        switch(cp.name)
        for item in shipsizes:
            cp.add_ship(item, args.auto)
#        print cp.grid

def switch(player_num):
    '''
    Clears screen and holds for player (player_num)
    '''
    clear_screen()
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
    parser.add_argument('-a', '--auto', action='store_true', default=False, help='Auto Place Ships Randomly?')
    args = parser.parse_args()
    return args

class Player:
    '''
    Player Class
    Contains Shiplist and Grid
    '''

    def __init__(self, gridsize, name):
        '''
        Initializes a Player
        '''
        self.gridsize = gridsize
        self.grid     = gen_grid(gridsize)
        self.guesses  = gen_grid(gridsize)
        self.shiplist = []
        self.name     = name
        self.state    = True

    def shoot(self, pid, coord):
        '''
        Shoot at specified player at specified coordinates
        '''
        [x, y] = coord.split(':')
        target = players[pid]
        for item in target.shiplist:
            result = item.register(x, y)
            if result == True:
                print 'Hit!'
                self.guesses[y][x] = 'X'
            elif result == False:
                print 'Miss!'
                self.guesses[y][x] = 1
            else:
                print result
                self.guesses[y][x] = 'X'
        print self.guesses

    def get_rand_pos(self):
        '''
        Returns a random spot
        '''
        if random.randint(0,1) == 0:
            ort = 'v'
        else:
            ort = 'h'
        coord = '%i:%i:%s' %(random.randint(0, self.gridsize),
                             random.randint(0, self.gridsize), ort)
        return coord

    def add_ship(self, size, auto):
        if auto:
            coord = self.get_rand_pos()
        else:
            coord = raw_input('Please Enter Location for Ship with Size %i (X:Y:R): ' %size)
        new_ship      = self.Ship(size, coord, self.gridsize)
        ship_conflict = new_ship.conflict(self.grid)
        while ship_conflict == True:
            if auto:
                coord = self.get_rand_pos()
            else:
                coord = raw_input('Please Enter Location for Ship with Size %i (X:Y:R): ' %size)
            new_ship      = self.Ship(size, coord, self.gridsize)
            ship_conflict = new_ship.conflict(self.grid)

        [x, y, r] = coord.split(':')
        x = int(x)
        y = int(y)

        for number in range(size):
            if r == 'v':
                    self.grid[y + number][x] = 1
            elif r == 'h':
                    self.grid[y][x + number] = 1

        self.shiplist.append(new_ship)
        if not auto:
            print self.grid


    class Ship:
        '''
        Ship Class
        '''

        def __init__(self, size, coord, gridsize):
            '''
            Initializes an Aircraft Carrier
            '''
            self.hits      = []
            self.x         = int(coord.split(':')[0])
            self.y         = int(coord.split(':')[1])
            self.r         = coord.split(':')[2]
            self.size      = size
            self.test_grid = gen_grid(gridsize)

        def register(self, x0, y0):
            '''
            Registers a hit (or a miss)
            '''
            sunk = 'You have sunk my ship! (%i)' %self.size
            for item in self.hits:
                if item == ('%i:%i' %(y0, x0)):
                    item = 0
                    flag = True
                    for item in self.hits:
                        if item != 0:
                            flag = False
                    if flag:
                        return sunk
                    else:
                        return True
            return False

        def conflict(self, grid):
            '''
            Determines if there's a conflict between two ships
            '''
            if self.r == 'v':
                try:
                    for number in range(self.size):
                        self.test_grid[self.y + number][self.x]
                        self.hits.append('%i:%i' %(self.y, self.x))
                except IndexError:
                    return True
            elif self.r == 'h':
                try:
                    for number in range(self.size):
                        self.test_grid[self.y][self.x + number]
                        self.hits.append('%i:%i' %(self.y, self.x))
                except IndexError:
                    return True
            else:
                return True

            for number in range(self.size):
                if self.r == 'v':
                    if grid[self.y + number][self.x] == 1:
                        return True
                elif self.r == 'h':
                    if grid[self.y][self.x + number] == 1:
                        return True
            return False

class Screen:

    def __init__(self):
        pygame.init()
        black  = (   0,   0,   0)
        white  = ( 255, 255, 255)
        green  = (   0, 255,   0)
        red    = ( 255,   0,   0)
        screen = pygame.display.set_mode([500,500])
        done   = False
        clock  = pygame.time.Clock()
        pygame.display.set_caption('BattleShip')
        while done == False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
            screen.fill(black)
            pygame.display.flip()
            clock.tick(20)

        pygame.quit()


if __name__=="__main__":
    sys.exit(main())
