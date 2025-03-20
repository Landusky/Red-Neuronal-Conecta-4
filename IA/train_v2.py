from conecta4 import Game, PlayerType
from minimax import MinimaxPlayer
from network import LearningPlayer
from const import *
import matplotlib.pyplot as plt
from tqdm import tqdm

p1 = MinimaxPlayer("Minimax")
p2 = LearningPlayer("IA")

ia_wins_partial = 0
ia_winrate = []
winrate_steps = []

for episode in tqdm(range(TRAIN_EPISODES)):

	p1.reset()
	p2.reset()
	game = Game(p1, p2)

	while not game.game_over:

		state = game.board # Tablero antes de ejecutar la acción

		if game.player_index == 1: # IA Player
			col = game.players[game.player_index].choose_action(state)
		else: # Minimax Player
			col = game.players[game.player_index].choose_action(game.board, PlayerType.PLAYER1, PlayerType.PLAYER2)

		action = col

		reward = game.turn(col)

		next_state = game.board # Tablero después de ejecutar la acción

		if game.player_index == 1:
			game.players[game.player_index].learn(state, action, reward, next_state)

	if (game.active_player == PlayerType.PLAYER2):
		ia_wins_partial += 1

	if ((episode+1) % 5) == 0:
		ia_winrate.append(ia_wins_partial / (episode+1) * 100)
		winrate_steps.append(episode+1)

p2.network.save_model('Trained_IA')

plt.plot(winrate_steps, ia_winrate, label = "IA Winrate")
plt.legend()
plt.show()

