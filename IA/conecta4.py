import numpy as np
from enum import IntEnum
from players import Player
from const import *


class PlayerType(IntEnum):
	PLAYER1 = -1 
	PLAYER2 = 1 # La IA siempre es el jugador 2



class Game:
	def __init__(self, player1:Player, player2:Player):  #Indica que player1/2 son de la clase Player
		self.board = np.zeros((ROW_COUNT,COLUMN_COUNT))
		self.game_over = False
		self.active_player = PlayerType.PLAYER1
		self.players = [player1, player2]
		self.player_index = 0	#Número para indicar el turno
		self.turn_count = 1		#Número para saber cuantos movimientos quedan por hacer

	def change_player(self):
		self.active_player = PlayerType.PLAYER2 if self.active_player==PlayerType.PLAYER1 else PlayerType.PLAYER1  #Utilización de if y else en una misma fila
		self.player_index += 1
		self.player_index %= 2

	def turn(self, col:int):	#Indica que col es un número
		if not self.is_valid_col(col):
			raise Exception("posición imposible")	#Peta el programa
		filed = self.drop_piece(col)	
		if self.winning_move():
			print(f"El jugador {self.players[self.player_index].name} ha ganado ")		#Imprime el jugador que había activo en ese momento
			self.game_over = True
			reward = self.active_player
		elif self.board.all() or self.turn_count >= MAX_TURNS: #Se ha llenado el tablero
			print("Empate")
			self.game_over = True
			reward = 0.5
		else:
			if filed:
				self.players[0].valid_actions.remove(col)	#Elimina de la lista de columnas posibles la columna que se ha llenado
				self.players[1].valid_actions.remove(col)
			self.change_player()
			self.turn_count += 1
			reward = 0
		return reward
		
	def place_piece(self, row:int, col:int, piece:int):
		self.board[row][col] = piece
	
	def drop_piece(self, col:int)->bool:		#indica que el resultado debe ser booleano
		if self.is_valid_col(col):
			row = self.get_next_open_row(col)
			self.place_piece(row, col, self.active_player)
			return row == 0


	def is_valid_col(self, col:int)->bool:
		return self.board[0][col] == 0

	def get_next_open_row(self, col:int)->int:
		for r in range(ROW_COUNT-1,-1,-1):
			if self.board[r][col] == 0:
				return r

	def print_board(self):
		print(self.board)


	def winning_move(self)->bool:
		# Check horizontal locations for win
		for c in range(COLUMN_COUNT-3):
			for r in range(ROW_COUNT):
				if self.board[r][c] == self.active_player and self.board[r][c+1] == self.active_player and self.board[r][c+2] == self.active_player and self.board[r][c+3] == self.active_player:
					return True

		# Check vertical locations for win
		for c in range(COLUMN_COUNT):
			for r in range(ROW_COUNT-3):
				if self.board[r][c] == self.active_player and self.board[r+1][c] == self.active_player and self.board[r+2][c] == self.active_player and self.board[r+3][c] == self.active_player:
					return True

		# Check positively sloped diaganols
		for c in range(COLUMN_COUNT-3):
			for r in range(ROW_COUNT-3):
				if self.board[r][c] == self.active_player and self.board[r+1][c+1] == self.active_player and self.board[r+2][c+2] == self.active_player and self.board[r+3][c+3] == self.active_player:
					return True

		# Check negatively sloped diaganols
		for c in range(COLUMN_COUNT-3):
			for r in range(3, ROW_COUNT):
				if self.board[r][c] == self.active_player and self.board[r-1][c+1] == self.active_player and self.board[r-2][c+2] == self.active_player and self.board[r-3][c+3] == self.active_player:
					return True


