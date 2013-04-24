#!/usr/bin/env python

import unittest
import battleship

class TestBattleship(unittest.TestCase):

    def __init(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)

    def setUp(self):
        '''
        Creates a couple players/games
        '''
        self.player1 = battleship.Player(10, 'one')

        self.player2 = battleship.Player(10, 'two')

        self.player3 = battleship.Player(10, 'three')
        self.player3.add_ship(5, True)
        self.player3.add_ship(3, True)
        self.player3.add_ship(9, True)
        self.player3.add_ship(8, True)
        self.player3.add_ship(1, True)
        self.player3.add_ship(2, True)
        self.player3.add_ship(7, True)

    def test_gen_grid(self):
        '''
        Asserts grid is fine
        '''
        assert(battleship.gen_grid(1) == [[0]])
        assert(len(battleship.gen_grid(2)) == 2)
        assert(len(battleship.gen_grid(2)[0]) == 2)
        assert(len(battleship.gen_grid(10)) == 10)
        assert(len(battleship.gen_grid(10)[0]) == 10)

    def test_player(self):
        '''
        Asserts Player is good
        '''
        sample_player = battleship.Player(10, 'test')
        assert(len(sample_player.grid) == 10)
        assert(len(sample_player.grid[0]) == 10)

    def test_ship(self):
        sample_ship = self.player1.Ship(3, '0:1:v', 10)
        assert(sample_ship.x == 0)
        assert(sample_ship.y == 1)
        assert(sample_ship.r == 'v')
        assert(len(sample_ship.test_grid) == 10)

    def test_add_ship(self):
        '''
        Tests a couple different player/ship combos
        '''
        self.player1.add_ship(3, True)
        self.player2.add_ship(3, True)

        self.player3.add_ship(3, True)
        self.player3.add_ship(5, True)
        self.player3.add_ship(3, True)
        self.player3.add_ship(9, True)
        self.player3.add_ship(8, True)
        self.player3.add_ship(1, True)
        self.player3.add_ship(2, True)
        self.player3.add_ship(7, True)

    def test_get_coords(self):
        assert(battleship.get_coords('sad') == False)
        assert(battleship.get_coords('0:4:2') == (0, 4, 2))
        assert(battleship.get_coords('A:0:3') == False)
        assert(battleship.get_coords('5:5:5') == (5, 5, 5))

    def test_get_state(self):
        assert(self.player3.get_state() == True)

if __name__ == "__main__":
    unittest.main()
