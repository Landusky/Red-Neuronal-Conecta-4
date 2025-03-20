from conecta4 import Game, PlayerType
from players import RandomPlayer
from minimax import MinimaxPlayer

p1 = RandomPlayer("Random")
p2 = MinimaxPlayer("Minimax", 2)
game = Game(p2, p1)
while not game.game_over:
	game.print_board()
	print(f"Turno del jugador {game.players[game.player_index].name}")

	if game.player_index == 0: # IA Player
		col = game.players[game.player_index].choose_action(game.board, PlayerType.PLAYER1, PlayerType.PLAYER2)
	else:
		col = game.players[game.player_index].choose_action()

	game.turn(col)
game.print_board()