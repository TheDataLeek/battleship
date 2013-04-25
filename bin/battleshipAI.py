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
        self.name      = player.name
        self.gridsize  = player.gridsize
        self.guesses   = player.guesses
        self.grid      = player.grid
        self.player    = player
        self.level     = random.randint(0, 2)
        self.last_shot = None

    def is_shot(self, x, y, gridsize, pid):
        '''
        Determines if we've shot this spot before
        '''
        for item in self.guesses:
            if item.pid == pid:
                current_guesses = item.guesses
        try:
            current_guesses[y][x]
            if current_guesses[y][x] != 0:
                return True
        except IndexError:
            return True
        return False

    def get_rand_spot(self, gridsize, pid):
        '''
        Gets a random spot and returns
        '''
        x = random.randint(0, gridsize - 1)
        y = random.randint(0, gridsize - 1)
        conflict = self.is_shot(x, y, gridsize, pid)
        while conflict:
            x = random.randint(0, gridsize - 1)
            y = random.randint(0, gridsize - 1)
            conflict = self.is_shot(x, y, gridsize, pid)
        return x, y

    def diagonal(self, gridsize, pid):
        '''
        Shoots in diagonal pattern
        '''
        corner = gridsize - 1
        if self.is_shot(0, corner, gridsize, pid):
            return False, False
        elif not self.is_shot(corner, corner, gridsize, pid):
            (x, y) = (0, 0)
            conflict = self.is_shot(x, y, gridsize, pid)
            while conflict:
                x += 1
                y += 1
                conflict = self.is_shot(x, y, gridsize, pid)
        elif self.is_shot(corner, corner, gridsize, pid):
            (x, y) = (corner, 0)
            conflict = self.is_shot(x, y, gridsize, pid)
            while conflict:
                x -= 1
                y += 1
                conflict = self.is_shot(x, y, gridsize, pid)
                if y == gridsize:
                    print('we should not be here')
                    break
        return x, y

    def follow(self, gridsize, pid):
        '''
        Follows a coordinate
        '''
        x = self.last_shot[0]
        y = self.last_shot[1]
        conflict = self.is_shot(x, y, gridsize, pid)
        num_list = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        while conflict:
            for number in range(len(num_list)):
                if num_list[number] is not None:
                    x += num_list[number][0]
                    y += num_list[number][1]
                    num_list[number] = None
                    conflict = self.is_shot(x, y, gridsize, pid)
                    if conflict:
                        x = self.last_shot[0]
                        y = self.last_shot[1]
                    else:
                        break
                elif num_list == [None, None, None, None]:
                    x, y = self.get_rand_spot(gridsize, pid)
                    conflict = False
        return x, y

    def get_position(self, playerlist):
        '''
        Shoots at a random player in a designated pattern
        '''
        pid = random.randint(0, len(playerlist) - 1)
        while playerlist[pid].state != True:
            pid = random.randint(0, len(playerlist) - 1)
        while pid == self.name:
            pid = random.randint(0, len(playerlist) - 1)
        if self.last_shot:
            x, y = self.follow(self.gridsize, pid)
        else:
            x, y = self.diagonal(self.gridsize, pid)
        if x is False or y is False:
            x, y = self.get_rand_spot(self.gridsize, pid)
        return pid, x, y

    def shoot(self, playerlist):
        '''
        Shoots at a player
        '''
        p, x, y = self.get_position(playerlist)
        target = playerlist[p]
        for item in self.guesses:
            if item.pid == p:
                current_guesses = item.guesses
        for item in target.shiplist:
            result = item.register(x, y)
            if result == True:
                current_guesses[y][x] = 1
                self.last_shot = (x, y)
                break
            elif result == False:
                current_guesses[y][x] = -1
                self.last_shot = None
            else:
                current_guesses[y][x] = 1
                self.last_shot = (x, y)
                break
