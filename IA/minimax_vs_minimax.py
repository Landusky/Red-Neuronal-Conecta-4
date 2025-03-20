from conecta4 import Game, PlayerType
from minimax import MinimaxPlayer

p1 = MinimaxPlayer("Minimax 1", 5)
p2 = MinimaxPlayer("Minimax 2", 5)
game = Game(p2, p1)

maximising_player = PlayerType.PLAYER1
minimising_player = PlayerType.PLAYER2

while not game.game_over:
	game.print_board()
	print(f"Turno del jugador {game.players[game.player_index].name}")

	col = game.players[game.player_index].choose_action(game.board, maximising_player, minimising_player)

	maximising_player, minimising_player = minimising_player, maximising_player

	game.turn(col)
game.print_board()