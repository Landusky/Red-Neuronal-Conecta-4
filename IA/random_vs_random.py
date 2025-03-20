from conecta4 import Game
from players import HumanPlayer, RandomPlayer

p1 = RandomPlayer("Jugador 1")
p2 = RandomPlayer("jugador 2")
game = Game(p1, p2)
while not game.game_over:
	game.print_board()
	print(f"Turno del jugador {game.players[game.player_index].name}")
	col = game.players[game.player_index].choose_action()
	game.turn(col)
game.print_board()