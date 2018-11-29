__author__ = 'gkour'

import numpy as np
import random
from brains.abstractbrain import AbstractBrain


class DNABrain(AbstractBrain):
    def __init__(self, dna):
        super(AbstractBrain, self).__init__()
        self._dna = dna

    def think(self, obs, eps=0):
        return np.random.choice(len(self._dna), 1, p=self._dna)

    def train(self, batch_obs, batch_acts, batch_rews, batch_newstate):
        pass

    def save_model(self, path):
        pass

    def load_model(self, path):
        pass


class RandomBrain(AbstractBrain):
    def __init__(self, action_size):
        super(AbstractBrain, self).__init__()
        self._action_size = action_size

    def think(self, obs, eps=0):
        return random.randint(0,self._action_size-1)

    def train(self, batch_obs, batch_acts, batch_rews, batch_newstate):
        pass

    def save_model(self, path):
        pass

    def load_model(self, path):
        pass
