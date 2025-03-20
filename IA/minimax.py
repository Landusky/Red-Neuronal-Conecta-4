from conecta4 import PlayerType
import math
import random
from const import *
from players import Player


def winning_move(board, player) -> bool:
	# Check horizontal locations for win
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT):
			if board[r][c] == player and board[r][c+1] == player and board[r][c+2] == player and board[r][c+3] == player:
				return True

	# Check vertical locations for win
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT-3):
			if board[r][c] == player and board[r+1][c] == player and board[r+2][c] == player and board[r+3][c] == player:
				return True

	# Check positively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT-3):
			if board[r][c] == player and board[r+1][c+1] == player and board[r+2][c+2] == player and board[r+3][c+3] == player:
				return True

	# Check negatively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(3, ROW_COUNT):
			if board[r][c] == player and board[r-1][c+1] == player and board[r-2][c+2] == player and board[r-3][c+3] == player:
				return True

def get_valid_locations(board):
	return [col for col in range(COLUMN_COUNT) if board[0][col] == 0]


def get_next_open_row(board, col:int) -> int:
	for r in range(ROW_COUNT-1,-1,-1):
		if board[r][col] == 0:
			return r

def score_position(board, piece):
	score = 0

	## Score Horizontal
	for r in range(ROW_COUNT):
		row_array = [int(i) for i in list(board[r,:])]
		score += sum(row_array)

	## Score Vertical
	for c in range(COLUMN_COUNT):
		col_array = [int(i) for i in list(board[:,c])]
		score += sum(col_array)

	## Score posiive sloped diagonal
	for r in range(ROW_COUNT):
		for c in range(COLUMN_COUNT):
			i = 0
			while r+i < ROW_COUNT and c+i < COLUMN_COUNT:
				score += board[r+i][c+i]
				i += 1

	## Score negative sloped diagonal
	for r in range(ROW_COUNT):
		for c in range(COLUMN_COUNT):
			i = 0
			while r-i >= 0 and c+i < COLUMN_COUNT:
				score += board[r-i][c+i]
				i += 1

	return score * int(piece)

def minimax(board, depth, maximizingPlayer, minimizingPlayer, isMaximizing):
	valid_locations = get_valid_locations(board)

	ia_wins = winning_move(board, maximizingPlayer)
	oponent_wins = winning_move(board, minimizingPlayer)

	is_terminal = ia_wins or oponent_wins or len(valid_locations) == 0

	if depth == 0 or is_terminal:
		if is_terminal:
			if ia_wins:
				return (None, math.inf)
			elif oponent_wins:
				return (None, -math.inf)
			else: # Game is over, no more valid moves
				return (None, 0)
		else: # Depth is zero
			return (None, score_position(board, maximizingPlayer))

	if isMaximizing:
		value = -math.inf
		column = random.choice(valid_locations)

		for col in valid_locations:
			b_copy = board.copy() # Copy the board

			# Simulate the move
			row = get_next_open_row(b_copy, col)
			b_copy[row][col] = maximizingPlayer

			# Call minimax recursively and choose the maximum value
			new_score = minimax(b_copy, depth-1, maximizingPlayer, minimizingPlayer, False)[1]

			if new_score > value:
				value = new_score
				column = col

		return column, value

	else: # Minimizing player
		value = math.inf
		column = random.choice(valid_locations)

		for col in valid_locations:
			b_copy = board.copy() # Copy the board

			# Simulate the move
			row = get_next_open_row(b_copy, col)
			b_copy[row][col] = minimizingPlayer

			# Call minimax recursively and choose the minimum value
			new_score = minimax(b_copy, depth-1, maximizingPlayer, minimizingPlayer, True)[1]

			if new_score < value:
				value = new_score
				column = col

		return column, value


class MinimaxPlayer(Player):
	def __init__(self, name:str, depth: int):
		super().__init__(name)
		self.depth = depth

	def choose_action(self, board, maximizingPlayer, minimizingPlayer)->int:
		return minimax(board, self.depth, maximizingPlayer, minimizingPlayer, True)[0]