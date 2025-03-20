
from random import choice, seed
from const import COLUMN_COUNT


class Player:
	def __init__(self, name:str):
		self.name = name
		self.valid_actions = list(range(COLUMN_COUNT))

	def choose_action(self)->int:
		pass

	def learn(self):
		pass

	def reset(self):
		self.valid_actions = list(range(COLUMN_COUNT))

class HumanPlayer(Player):
	def __init__(self, name:str):
		super().__init__(name)
	
	def choose_action(self)->int:
		col = int(input(f"Columna del 0 al {COLUMN_COUNT-1}: ")) #Asumimos que es un número
		while col < 0 or col > 6 or col not in self.valid_actions:
			col = int(input(f"Error. Columna del 0 al {COLUMN_COUNT-1}: "))
		return col

class RandomPlayer(Player):
	def __init__(self, name:str):
		super().__init__(name)
		#seed(42)  # DEBUG
	
	def choose_action(self)->int:
		col = choice(self.valid_actions)
		return col