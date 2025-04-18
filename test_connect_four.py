import unittest
from copy import deepcopy

from connect_four_final import count_star_in_column, place_counter, player_won
class TestConnectFour(unittest.TestCase):
    
    @classmethod
    def setUp(self):
        global computer_counter
        mode = 'None ' # Reset mode to avoid stale values from other tests
        computer_counter = 'Y'
        self.empty_board = [["*"] * 7 for _ in range(6)]    #Create empty board
        self.partial_board = deepcopy(self.empty_board)     #Create deepcopy of empty board
        self.partial_board[5][0] = 'R'                      #Fill deepcopy with some counters
        self.partial_board[4][0] = 'Y'
        self.partial_board[3][0] = 'R'

    def test_count_star_in_column(self):
        global computer_counter
        self.assertEqual(count_star_in_column(self.empty_board, 1), 6)          #Check the count_star_in_column function
        self.assertEqual(count_star_in_column(self.partial_board, 1), 3)

    def test_place_counter_full_column(self):
        global computer_counter
        mode = 'B'
        computer_counter = 'Y'
        board = [['R'] * 7 for _ in range(6)]              #Creating a full board
        result = place_counter(board, 1, 'Y', mode)        #Trying to place a counter on a full board
        self.assertFalse(result)

    def test_player_won_horizontal(self):
        global computer_counter
        board = deepcopy(self.empty_board)
        for i in range(4):
            board[5][i] = 'R'                              #Filling a row with the 'R' counter
        self.assertTrue(player_won(board, 'R'))            #Checking this wins the game

    def test_player_won_vertical(self):
        global computer_counter
        board = deepcopy(self.empty_board)
        for i in range(4):
            board[5 - i][0] = 'Y'                          #Filling a column with the 'Y' counter
        self.assertTrue(player_won(board, 'Y'))            #Checking this wins the game

    def test_player_won_diagonal_down(self):
        global computer_counter
        board = deepcopy(self.empty_board)
        for i in range(4):
            board[2 + i][i] = 'R'                         #Filling a downward diagonal with the 'R' counter
        self.assertTrue(player_won(board, 'R'))           #Checking this wins the game

    def test_player_won_diagonal_up(self):
        global computer_counter
        board = deepcopy(self.empty_board)
        for i in range(4):
            board[5 - i][i] = 'Y'                         #Filling an upward diagonal with the 'Y' counter
        self.assertTrue(player_won(board, 'Y'))           #Checking this wins the game

    @classmethod
    def tearDownClass(cls): 
        print("All tests for the Connect Four game have now completed.")

#Running the tests
if __name__ == '__main__':
    unittest.main()
