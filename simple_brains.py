__author__ = 'gkour'

import numpy as np
import random


class DNABrain:
    def __init__(self, dna):
        self._dna = dna

    def decide_on_action(self, state):
        return np.random.choice(len(self._dna), 1, p=self._dna)


class RandomBrain:
    def __init__(self, action_size):
        self._action_size = action_size

    def decide_on_action(self, state):
        return random.randint(0,self._action_size-1)
