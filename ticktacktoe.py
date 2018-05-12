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
		self._rows=rows
		self._cols=cols
		# the thing that contains the Xs and Os
		self.boardStatus = np.reshape(np.zeros(self._rows * self._cols,dtype=int), (self._rows, self._cols))

	@property
	def rows(self):
		return self._rows
	@property
	def cols(self):
		return self._cols

	def get_board(self):
		return self.boardStatus
	def set_board(self,board):
		self.boardStatus=board

	def _valid_point(self,row,col):
		return 0 <= row < self.rows and 0 <= col < self._cols

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

		for piece in [self.type["x"],self.type["o"]]:
			for row,col in [(row,col) for row in range(self.rows) for col in range(self._cols)]:
				left_right = lambda row,col,direction: (row,direction+col)
				up_down = lambda row,col,direction: (row+direction,col)
				diag_up_right = lambda row,col,direction: (row-direction,col+direction)
				diag_down_right = lambda row,col,direction: (row+direction,col+direction)
				def test_points(points,type):
					for point in points:
						if self.boardStatus[point] != type:
							return False
					return True
				for movement in [left_right, up_down, diag_up_right, diag_down_right]:
					points=get_test_squares(row,col,movement)
					if len(points) >= self.win_length and test_points(points,piece):
						return piece
		return self.type["blank"]


class test_tick_tack_toe_board(unittest.TestCase):
	def test_1(self):
		board=tick_tack_toe_board()
		self.assertFalse( board.game_won() )
		for row,col in ((0,0),(1,1),(2,2)):
			board.boardStatus[row][col] = board.type["x"]
		self.assertEqual( board.game_won(), board.type["x"])
		self.assertNotEqual( board.game_won(), board.type["o"])

def get_tack_tack_toe_losing_move(board, toMove=None):
	"""
	Returns a (row,col) tuple for the move that'll be guaranteed to make the current mover loose or None if no such move exists
	"""
	# can't get a losing move if the game is won
	if board.game_won() == toMove:
		return None

	cur_pos = board.get_board()

	def try_next(pos,increment=False):
		row,col=pos
		if increment:
			col += 1
		# keep looking for avaliable spots untill a blank spot is fount
		while board.boardStatus[row,col] != board.type["blank"]:
			if col >= board.cols:
				row+=1
				col=0
			if row >= board.rows:
				return None
		return row,col

	attempt_move=try_next( (0,0) )
	while attempt_move is not None:
		board.boardStatus[attempt_move] = {board.type("x"):board.type["o"],board.type("o"):board.type["x"]}[toMove]
		result = get_tack_tack_toe_losing_move(board,toMove)
		if result is not None:
			return attempt_move
		# if the move doesn't give us what we want try again with soething else
		board.set_board(cur_pos)
		attempt_move=try_next(attempt_move,increment=True)
	# if we didn't return a valid move in the loop there is none to be found
	return None

class test_get_tack_tack_toe_losing_move(unittest.TestCase):
	def test_1(self):
		def get_result( x_moves, o_moves,toMove=None):
			board=tick_tack_toe_board()
			for xmove in x_moves:
				board.boardStatus[xmove]=board.type["x"]
			for omove in o_moves:
				board.boardStatus[omove]=board.type["o"]
			return get_tack_tack_toe_losing_move(board,toMove)
		self.assertEquals( None, get_result([(0,0),(0,1),(1,2),(2,0)],[(0,2),(1,0),(1,1)] ))


if __name__== '__main__':
	unittest.main()