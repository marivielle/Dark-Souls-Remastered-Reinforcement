#Mariana Capdevielle Schurmann - c1830536

"""Reinforcement learning model"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam

from collections import deque, namedtuple

from keras import backend as K
import numpy as np
import random
from env import DarkSoulsEnv


class Agent:
    def __init__(self, action_size, state_size, dims):
        self.action_size = action_size
        self.state_size = state_size
        self.dims = dims
        self.memory = deque(maxlen=5000)
        self.learning_rate = 0.001
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_interval = 0.99
        self.gamma = 0.95
        self.model = self.build_model()
        self.target_model = self.build_model()
        self.update_target_model()

    def huber_loss(self, y_true, y_pred, clip_delta=1.0):
        error = y_true - y_pred
        cond = K.abs(error) <= clip_delta

        squared_loss = 0.5 * K.square(error)
        quadratic_loss = 0.5 * K.square(clip_delta) + clip_delta * (K.abs(error) - clip_delta)

        return K.mean(tf.where(cond, squared_loss, quadratic_loss))

    def build_model(self):
        model = Sequential()
        #model.add(Flatten(input_shape=(1, self.state_size)))
        model.add(Dense(self.dims[0], input_dim=self.state_size, activation='relu'))
        #model.add(Dense(self.dims[0], activation='relu'))
        model.add(Dense(self.dims[1], activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))

        model.compile(loss=self.huber_loss, optimizer=Adam(learning_rate=self.learning_rate))

        return model

    def update_target_model(self):
        # copy weights from model to target_model
        self.target_model.set_weights(self.model.get_weights())

    def memorize(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])  # returns action

    def replay(self, batch_size):
        #sample batch from memory
        batch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in batch:
            target = self.model.predict(state)
            if done:
                target[0][action] = reward
            else:
                t = self.target_model.predict(next_state)[0]
                target[0][action] = reward + self.gamma * np.amax(t)
            self.model.fit(state, target, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_interval

    def load(self, name):
        self.model.load_weights(name)

    def save(self, name):
        self.model.save_weights(name)


class ReplayBuffer: #attempt at experience replay with prioritised learning
    def __init__(self, seed, mem_size=int(1e5), batch=32):
        self.buffer_size = mem_size
        self.state_mem = np.zeros((self.buffer_size, *DarkSoulsEnv.observation_space.shape), dtype=np.float32)
        self.action_mem = np.zeros(self.buffer_size, dtype=np.int32)
        self.reward_mem = np.zeros(self.buffer_size, dtype=np.float32)
        self.next_state_mem = np.zeros((self.buffer_size, *DarkSoulsEnv.observation_space.shape), dtype=np.float32)
        self.done_mem = np.zeros(self.buffer_size, dtype=np.bool)
        self.pointer = 0

    def store(self, state, action, reward, state_, priority, done):
        idx = self.pointer % self.buffer_size
        self.state_mem[idx] = state
        self.action_mem[idx] = action
        self.reward_mem[idx] = reward
        self.next_state_mem[idx] = state_
        self.done_mem[idx] = 1 - int(done)
        self.pointer += 1

    def update_priorities(self, batch_indices, batch_priorities):
        for idx, prio in zip(batch_indices, batch_priorities):
            self.priorities[idx] = prio

    def sample(self, batch_size):
        max_mem = min(self.pointer, self.buffer_size)
        batch = np.random.choice(max_mem, batch_size, replace=False)
        states = self.state_mem[batch]
        actions = self.action_mem[batch]
        rewards = self.reward_mem[batch]
        next_states = self.next_state_mem[batch]
        dones = self.done_mem[batch]

        return states, actions, rewards, next_states, dones
