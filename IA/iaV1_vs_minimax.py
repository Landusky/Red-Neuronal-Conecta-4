from conecta4 import Game, PlayerType
from network import IAPlayer
from minimax import MinimaxPlayer

p1 = MinimaxPlayer("Minimax")
p2 = IAPlayer("IA", "Trained_IA.h5")
game = Game(p1, p2)
while not game.game_over:
	game.print_board()
	print(f"Turno del jugador {game.players[game.player_index].name}")

	if game.player_index == 0: # Minimax Player
		col = game.players[game.player_index].choose_action(game.board, PlayerType.PLAYER1, PlayerType.PLAYER2)
	else: # IA Player
		col = game.players[game.player_index].choose_action(game.board)

	game.turn(col)
game.print_board()