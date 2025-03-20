from conecta4 import Game
from players import HumanPlayer
from network import IAPlayer

p1 = HumanPlayer("Jugador 1")
p2 = IAPlayer("IA", "Trained_IA.h5")
game = Game(p1, p2)
while not game.game_over:
	game.print_board()
	print(f"Turno del jugador {game.players[game.player_index].name}")
	
	if game.player_index == 1: # IA Player
		col = game.players[game.player_index].choose_action(game.board)
	else:
		col = game.players[game.player_index].choose_action()

	game.turn(col)
game.print_board()