#!/usr/bin/env python

import random

class BattleshipAI:
    '''
    AI for Battleship
    '''

    def __init__(self, player):
        '''
        Artificial Intelligence Player for Battleship
        '''
        self.name     = player.name
        self.gridsize = player.gridsize
        self.guesses  = player.guesses
        self.grid     = player.grid
        self.player   = player

    def get_rand_spot(self, gridsize, pid):
        '''
        Gets a random spot and returns
        '''
        x = random.randint(0, gridsize - 1)
        y = random.randint(0, gridsize - 1)
        for item in self.guesses:
            if item.pid == pid:
                current_guesses = item.guesses
        while current_guesses[y][x] != 0:
            x = random.randint(0, gridsize - 1)
            y = random.randint(0, gridsize - 1)
        return x, y

    def random(self, playerlist):
        '''
        Shoots at a random player
        '''
        pid = random.randint(0, len(playerlist) - 1)
        while playerlist[pid].state != True:
            pid = random.randint(0, len(playerlist) - 1)
        while pid == self.name:
            pid = random.randint(0, len(playerlist) - 1)
        x, y = self.get_rand_spot(self.gridsize, pid)
        return pid, x, y

    def shoot(self, playerlist):
        '''
        Shoots at a player
        '''
        p, x, y = self.random(playerlist)
        target = playerlist[p]
        for item in self.guesses:
            if item.pid == p:
                current_guesses = item.guesses
        for item in target.shiplist:
            result = item.register(x, y)
            if result == True:
                current_guesses[y][x] = 1
#                self.player.guesses[y][x] = 1
                break
            elif result == False:
                current_guesses[y][x] = -1
#                self.player.guesses[y][x] = -1
            else:
                current_guesses[y][x] = 1
#                self.player.guesses[y][x] = 1
                break
