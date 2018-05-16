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
		""" checks to see if the game is won. Returns the winner or self.type["blank"] if no winner"""
		# This gets squares that go through a given row and column in a line
		def get_test_squares(row,col,movement):
			points=[(row,col)]
			for direction in [-1,1]:
				displacement=1
				while True:
					test_point=movement(row,col,displacement*direction)
					if test_point in self:
						displacement += 1
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
				# sees if all the points are of the given type
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

	def game_draw(self):
		""" Return true if the game is a draw and false otherwise """
		for num in np.ravel(self.boardStatus):
			if num == self.type["blank"]:
				return False
		if self.game_won() != self.type["blank"]:
			return False
		return True

	def __str__(self):
		string=""
		for row in range(self.rows):
			for col in range(self.cols):
				dock={self.type['x']:'x',self.type['o']:'o',self.type['blank']:' ' }
				string += str(dock[self.boardStatus[row,col]])+' '
			string += '\n'
		return string

class test_tick_tack_toe_board(unittest.TestCase):
	def test_1(self):
		board=tick_tack_toe_board()
		self.assertFalse( board.game_won() )
		for row,col in ((0,0),(1,1),(2,2)):
			board.boardStatus[row][col] = board.type["x"]
		self.assertEqual( board.game_won(), board.type["x"])
		self.assertNotEqual( board.game_won(), board.type["o"])
		self.assertEqual( board.game_draw(), False)
	def test_2(self):
		board=tick_tack_toe_board()
		self.assertFalse( board.game_won() )
		for row,col in ((0,0),(0,1),(2,0),(1,2),(2,1)):
			board.boardStatus[row][col] = board.type["x"]
		for row,col in ((1,1),(0,2),(1,0),(2,2)):
			board.boardStatus[row][col] = board.type["o"]
		self.assertEqual( board.game_won(), False)
		self.assertEqual( board.game_draw() , True)


def get_tack_tack_toe_losing_move(board, toMove=None):
	"""
	Returns a (row,col) tuple for the move that'll be guaranteed to make the current mover loose or None if no such "perfect" move exists
	"""
	# provides a way to alternate between Xs and Os
	next_type = lambda curType:  {board.type["x"]:board.type["o"],board.type["o"]:board.type["x"]}[toMove]

	# condition for when a game is won
	def game_won(board, toMove):
		return board.game_won() == next_type(toMove)
	def game_lost(board, toMove):
		return board.game_won() == toMove or board.game_draw()

	# condition for already lost and won
	if game_lost(board,toMove):
		return None

	cur_pos = board.get_board()

	# provides a way of iterating through avaliable positions on the board - this returns the next avaliable position to place a piece on the board
	def get_next(pos, exclusive=False):
		row,col=pos
		# increment the colummn before checking it if it's exclusive
		if exclusive:
			col += 1
		# keep looking for avaliable spots untill a blank spot is fount or we're out of locations
		while True:
			# correct things if they've gone out of bounds
			if col >= board.cols:
				row+=1
				col=0
				if row >= board.rows:
					return None
			# see if the location is avaliable
			if board.boardStatus[row,col] == board.type["blank"]:
				return row,col
			# the location get's checked before incrementing
			col += 1

	# gets a list of possible moves
	def get_possible_moves():
		moves=[]
		attempt_move=get_next( (0,0), exclusive=False )
		while attempt_move is not None:
			moves.append(attempt_move)
			attempt_move=get_next(attempt_move,exclusive=True)
		return moves

	def reset_board():
		board = cur_pos

	# make sure none of the following opponent moves have guaranteed victory
	for attempt_move in get_possible_moves():
		board.boardStatus[attempt_move] = toMove
		# If the move isn't good then try another
		if game_lost(board,toMove):
			reset_board()
			continue
		# also see if the move makes the player win
		if game_won(board,toMove):
			reset_board()
			return attempt_move
		# the move will win the game
		sucess=True
		# keep track of the status before making oponent moves
		last_status = board.boardStatus
		# no matter what the oposition does the player must still be able to "win" after their move
		for opposition_move in get_possible_moves():
			board.boardStatus[opposition_move]=next_type(toMove)
			# a win isn't that remarkable; we must win all possible oponent moves
			if game_won(board,toMove):
				board.boardStatus=last_status
				continue
			# alternatively, if there's no sure way of winning then the game is lost
			else:
				reset_board()
				sucess=False
				break

		# set up for next round
		reset_board()
		if sucess:
			return attempt_move

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
			print(board)
			return get_tack_tack_toe_losing_move(board,toMove)
		bord=tick_tack_toe_board()
		self.assertEqual( None, get_result([(0,0),(0,1),(1,2),(2,0)],[(0,2),(1,0),(1,1)],toMove=bord.type["x"] ))
		self.assertEqual( (1,2) , get_result([(0,0),(0,1),(1,0),(2,1)],[(0,2),(1,1),(2,2)],bord.type["x"]) )


if __name__== '__main__':
	unittest.main()