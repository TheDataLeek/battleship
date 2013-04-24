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
import time

try:
    import pygame
    from pygame import Color, Rect, Surface

    import numpy
    import scipy.misc
    import argparse
except ImportError:
    print 'Error, Missing Libraries'
    sys.exit(0)

players = []

def main():
    args = get_args()

    clear_screen()

    establish_players(args)

    initialize_game(args)

    start_game(args)

    end_game(args)

def end_game(args):
    '''
    Declares Winner and Ends Game
    '''
    clear_screen()
    for player in players:
        if player.get_state:
            print('Congratulations Player %i! You have won!' %player.name)

    for player in players:
        print("Player %i's ships: %s\nPlayer %i's guesses: %s"
                %(player.name, str(player.grid), str(player.guesses)))

def start_game(args):
    '''
    Starts gameplay
    '''
    num_playing = len(players);

    while num_playing >= 2:
        #Each player shoots
        for player in players:
            # Display This player must play
            switch(player.name)
            print(player.guesses)
            # Display this player's guess grid
            p, x, y, = get_coords(player, args)
            player.shoot(p,x,y)
            raw_input("Press enter for next player")
        #Check if dead
        num_playing = 0;
        for p in players:
            if p.get_state:
                num_playing += 1

def split_coords(usr_string):
    '''
    Gets user input and returns coordinates
    '''
    try:
        p = int(usr_string.split(':')[0])
        x = int(usr_string.split(':')[1])
        y = int(usr_string.split(':')[2])
        return p, x, y
    except ValueError:
        return 0, -1, -1

def get_coords(player, args):
    '''
    Validates proper shooting input
    '''
    p, x, y = split_coords(
            raw_input(
                "Choose target player id and coordinates of shot (P:X:Y): "))
    while not players[p].get_state or p > len(players) or p < 0:
        p, x, y = split_coords(
                    raw_input(
                        "Invalid Player Id: Choose another set for your shot: "))
    while p == player.name:
        p, x, y = split_coords(
                    raw_input(
                          "Pew Pew Pew! You just tried to shoot yourself: Choose another set for your shot: "))

    while (x < 0 or x > (args.gridsize - 1) or
            y < 0 or y > (args.gridsize - 1)):
        p, x, y = split_coords(
                    raw_input(
                          "Invalid Coordinates: Choose another set for your shot: "))

    return p, x, y

def establish_players(args):
    '''
    Determines players/adds to listing
    '''
    if args.players < 2:
        ans = raw_input('Error, AI not enabled or invalid player count... Continue? (y/n) ')
        if ans.lower() == 'y':
            args.players = 2
        else:
            sys.exit(0)

    for number in range(args.players):
        new_player = Player(args.gridsize, number)
        players.append(new_player)

def initialize_game(args):
    '''
    Sets up the board for the player
    '''
    shipsizes = [5, 4, 3, 3, 2]
    for cp in players:
        switch(cp.name)
        for item in shipsizes:
            cp.add_ship(item, args.auto)
        print cp.grid
        raw_input("Continue")
    clear_screen()

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

    def shoot(self, pid, x , y):
        '''
        Shoot at specified player at specified coordinates
        '''

        target = players[pid]
        for item in target.shiplist:
            result = item.register(x, y)
            if result == True:
                print 'Hit!'
                self.guesses[y][x] = 1
                return
            elif result == False:
                self.guesses[y][x] = -1
            else:
                print result
                self.guesses[y][x] = 1
        print 'Miss!'

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
        start_time = time.time()
        while ship_conflict == True:
            current_time = time.time()
            if current_time - start_time > 10:
                print("Timout Error")
                sys.exit(0)
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

    def get_state(self):
        '''
        Refreshes state and returns
        '''
        if not self.state:
            return self.state
        else:
            for ship in self.shiplist:
                ship_state = False
                for item in ship.hits:
                    if item != 0:
                        ship_state = True
                self.state = ship_state
            return self.state

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
            self.state = True

        def register(self, x0, y0):
            '''
            Registers a hit (or a miss)
            '''
            hit_confirm = False
            for i in range(len(self.hits)):
                if self.hits[i] == ('%i:%i' %(y0, x0)):
                    self.hits[i] = 0
                    hit_confirm = True

            if hit_confirm == True:
                self.state = False
                for item in self.hits:
                    if item != 0:
                        self.state = True
                if self.state == False:
                    print 'You have sunk my ship! (%i)' %self.size
            
            return hit_confirm

        def conflict(self, grid):
            '''
            Determines if there's a conflict between two ships
            '''
            if self.r == 'v':
                try:
                    for number in range(self.size):
                        self.test_grid[self.y + number][self.x]
                        self.hits.append('%i:%i' %(self.y + number, self.x))
                except IndexError:
                    return True
            elif self.r == 'h':
                try:
                    for number in range(self.size):
                        self.test_grid[self.y][self.x + number]
                        self.hits.append('%i:%i' %(self.y, self.x + number))
                except IndexError:
                    return True
            else:
                return True

            for number in range(self.size):
                if self.r == 'v':
                    if grid[self.y + number][self.x] > 0:
                        return True
                elif self.r == 'h':
                    if grid[self.y][self.x + number] > 0:
                        return True
            return False

class Screen:
    def __init__(self, player_list):
        pygame.init()
        black  = (   0,   0,   0)
        white  = ( 255, 255, 255)
        green  = (   0, 255,   0)
        red    = ( 255,   0,   0)
        screen = pygame.display.set_mode([550,550])
        done   = False
        clock  = pygame.time.Clock()
        width  = 500 / player_list[0].gridsize
        height = 500 / player_list[0].gridsize
        margin = 5
        pygame.display.set_caption('BattleShip')

        while done == False:
            for item in player_list:
                if item.state == False:
                    done = True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
            screen.fill(black)
            player = player_list[0]
            gscr = scipy.misc.imresize(player.grid, 10.0)
            for row in range(len(gscr)):
                for entry in range(len(gscr[0])):
                    if gscr[row][entry] != 0:
                        gscr[row][entry] = 255
            grid_surface = pygame.surfarray.make_surface(gscr)
            screen.blit(grid_surface, (0,0))
            player = player_list[1]
            gscr = scipy.misc.imresize(player.grid, 10.0)
            for row in range(len(gscr)):
                for entry in range(len(gscr[0])):
                    if gscr[row][entry] != 0:
                        gscr[row][entry] = 255
            grid_surface = pygame.surfarray.make_surface(gscr)
            screen.blit(grid_surface, (0, 200))
            pygame.display.flip()
            clock.tick(10)

        pygame.quit()


if __name__=="__main__":
    sys.exit(main())
