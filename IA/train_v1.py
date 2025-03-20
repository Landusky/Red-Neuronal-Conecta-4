from conecta4 import Game, PlayerType
from players import HumanPlayer, RandomPlayer
from network import LearningPlayer
from const import *
import matplotlib.pyplot as plt
from tqdm import tqdm

p1 = RandomPlayer("Random")
p2 = LearningPlayer("IA")

ia_wins_partial = 0
ia_winrate = []
random_wins_partial = 0
random_winrate = []
winrate_steps = []

for episode in tqdm(range(TRAIN_EPISODES)):

	p1.reset()
	p2.reset()
	game = Game(p1, p2)

	while not game.game_over:

		state = game.board # Tablero antes de ejecutar la acción

		if game.player_index == 1: # IA Player
			col = game.players[game.player_index].choose_action(state)
		else:
			col = game.players[game.player_index].choose_action()

		action = col

		reward = game.turn(col)

		next_state = game.board # Tablero después de ejecutar la acción
		
		if game.player_index == 1:
			game.players[game.player_index].learn(state, action, reward, next_state)
	
	if (game.active_player == PlayerType.PLAYER2):
		ia_wins_partial += 1
	elif (game.active_player == PlayerType.PLAYER1):
		random_wins_partial += 1
	
	if ((episode+1) % 5) == 0:
		ia_winrate.append(ia_wins_partial / (episode+1) * 100)
		random_winrate.append(random_wins_partial / (episode+1) * 100)
		winrate_steps.append(episode+1)

p2.network.save_model('Trained_IA')

plt.plot(winrate_steps, ia_winrate, label = "IA Winrate")
plt.plot(winrate_steps, random_winrate, label = "Random Winrate")
plt.legend()
plt.show()

