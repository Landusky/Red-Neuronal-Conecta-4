from random import random, choice, sample
from keras.models import Sequential, load_model
from keras.layers import Flatten, Dense
from keras.optimizers import Adam
from const import *
from collections import deque
from players import Player

class Network:
    def __init__(self):
        self.model= Sequential()
        self.model.add(Flatten(input_shape = (ROW_COUNT, COLUMN_COUNT)))
        self.model.add(Dense(HIDDEN_LAYER_NEURON, activation="relu"))
        self.model.add(Dense(HIDDEN_LAYER_NEURON, activation="relu"))
        self.model.add(Dense(HIDDEN_LAYER_NEURON, activation="relu"))
        self.model.add(Dense(COLUMN_COUNT, activation="linear"))
        self.model.compile(loss="mse", optimizer=Adam(learning_rate = LEARNING_RATE ))

        self.memory = deque(maxlen = MEMORY_SIZE)
        self.exploration_rate = EXPLORATION_MAX

    def choose_action(self, state, valid_actions):
        if random()<= self.exploration_rate:
            col = choice(valid_actions)
            return col
        
        q_values = self.model.predict(state,  verbose=0)[0] #Elige de la lista la primera predicción
        columns = {i: q_values[i] for i in valid_actions} #Crea un diccionario con las columna validas y su probabilidad, pero manteniendo su posicion en el dict. (columna 2, en la posicion 1)
        col = max(columns, key = columns.get) #Te da la clave que tiene el valor más alto
        return col

    def learn(self):
        if len(self.memory)< BATCH_SIZE:
            return
        batch = sample(self.memory, BATCH_SIZE)
        for state, action, reward, next_state in batch:
            q_update = reward + GAMMA * max(self.model.predict(next_state, verbose=0)[0])
            q_values = self.model.predict(state, verbose=0)
            q_values[0][action] = q_update
            self.model.fit(state, q_values, verbose=0)
    
    def remember(self, state, action, reward, next_state):
        self.memory.append((state, action, reward, next_state))

    def save_model(self, file_prefix: str):
        self.model.save(f"{file_prefix}.h5")
    
    def update_exploration_rate(self):
        self.exploration_rate *= EXPLORATION_DECAY
        self.exploration_rate = max(EXPLORATION_MIN, self.exploration_rate)

class LearningPlayer(Player):
    def __init__(self, name:str):
        super().__init__(name)
        self.network = Network()

    def learn(self, state, action, reward, next_state):
        state = state.reshape(-1, ROW_COUNT, COLUMN_COUNT)
        next_state = next_state.reshape(-1, ROW_COUNT, COLUMN_COUNT)

        self.network.remember(state, action, reward, next_state)
        self.network.learn()
        self.network.update_exploration_rate()

    def choose_action(self, state)->int:
        state = state.reshape(-1, ROW_COUNT, COLUMN_COUNT)
        col = self.network.choose_action(state, self.valid_actions)
        return col

class IAPlayer(Player):
    def __init__(self, name:str, path_to_model):
        super().__init__(name)
        self.model = load_model(path_to_model)

    def choose_action(self, state) -> int:
        state = state.reshape(-1, ROW_COUNT, COLUMN_COUNT)

        q_values = self.model.predict(state,  verbose=0)[0] # Elige de la lista la primera predicción
        columns = {i: q_values[i] for i in self.valid_actions} # Crea un diccionario con las columna validas y su probabilidad, pero manteniendo su posicion en el dict. (columna 2, en la posicion 1)
        col = max(columns, key = columns.get) # Te da la clave que tiene el valor más alto
        return col