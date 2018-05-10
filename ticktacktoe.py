#!/usr/bin/env python

import numpy as np
import unittest
import pyphil

class tick_tack_toe_board:
	"""
	Does things pertaining to current board position. X moves first, O moves second in all cases.
	X and O are represented by the type variable
	"""
	def __init__(self,rows=3,cols=3):
		# for printing the board
		self.VERT=u'︱'
		self.HOR='_'
		# contains the location of X and 0
		self.grid=np.zeros(shape=(rows,cols))
		# the enumerated type for X or O
		self.type={'blank':0,'x':1,'o':2}
		# The length of "in a row" to win
		self.win_length=3
		self.rows=rows
		self.cols=cols
		# the thing that contains the Xs and Os
		self.board = np.reshape(np.zeros(self.rows*self.cols),(self.rows,self.cols))

	def _valid_point(self,row,col):
		return 0 <= row < self.rows and 0 <= col < self.cols

	def __contains__(self, point):
		return self._valid_point(point[0],point[1])

	def game_won(self):
		""" checks to see if the game is won. Returns the winner or 0 if no winner"""
		# This gets squares that go through a given row and column in a line
		def get_test_squares(row,col,movement):
			points=[(row,col)]
			displacement=1
			for direction in [-1,1]:
				while True:
					test_point=movement(row,col,displacement*direction)
					if test_point in self:
						direction += 1
						points.append( test_point)
					else:
						break
			return points

		for type in [self.type["x"],self.type["o"]]:
			for row,col in [(row,col) for row in range(self.rows) for col in range(self.cols)]:
				left_right = lambda row,col,direction: (row,direction+col)
				up_down = lambda row,col,direction: (row+direction,col)
				diag_up_right = lambda row,col,direction: (row-direction,col+direction)
				diag_down_right = lambda row,col,direction: (row+direction,col+direction)
				def test_points(points,type):
					for point in points:
						if self.board[point] != type:
							return False
					return True
				for movement in [left_right, up_down, diag_up_right, diag_down_right]:
					points=get_test_squares(row,col,movement)
					if len(points) >= self.win_length and test_points(points,type):
						return type
		return self.type["blank"]



	def get_move_history(self):
		return self.history;

class tick_tack_toe_game_generator:
	"""
	Generates possible tick tack toe games
	"""
	def generate_solutions(self,rows,cols):
		pass


class test_tick_tack_toe_board(unittest.TestCase):
	def test_1(self):
		board=tick_tack_toe_board()
		self.assertFalse( board.game_won() )
		for row,col in ((0,0),(1,1),(2,2)):
			board.board[row][col] = board.type["x"]
		self.assertEqual( board.game_won(), board.type["x"])

if __name__== '__main__':
	unittest.main()