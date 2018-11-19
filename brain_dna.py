__author__ = 'gkour'

import numpy as np


class Brain:
    def __init__(self, dna):
        self._dna = dna

    def decide_on_action(self, state):
        return np.random.choice(len(self._dna), 1, p=self._dna)
