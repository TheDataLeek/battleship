#!/usr/bin/env python

import random

class BattleshipAI:

    def __init__(self, player):
        '''
        Artificial Intelligence Player for Battleship
        '''
        self.name     = player.name
        self.gridsize = player.gridsize
        self.guesses  = player.guesses
        self.grid     = player.grid

    def get_rand_spot(self, gridsize):
        '''
        Gets a random spot and returns
        '''
        x = random.randint(0, gridsize - 1)
        y = random.randint(0, gridsize - 1)
        while self.guesses[y][x] != 0:
            x = random.randint(0, gridsize - 1)
            y = random.randint(0, gridsize - 1)
        return x, y

    def random(self, playerlist):
        '''
        Shoots at a random player
        '''
        pid = random.randint(0, len(playerlist) - 1)
        while pid == self.name:
            pid = random.randint(0, len(playerlist) - 1)
        x, y = self.get_rand_spot(self.gridsize)
        return pid, x, y

    def shoot(self, playerlist):
        '''
        Shoots at a player
        '''
        p, x, y = self.random(playerlist)
        target = playerlist[p]
        for item in target.shiplist:
            result = item.register(x, y)
            if result:
                self.guesses[y][x] = 1
            elif not result:
                self.guesses[y][x] = -1
