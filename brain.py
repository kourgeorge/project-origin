import numpy as np


class Brain:
    def __init__(self, dna):
        self._dna = dna

    def decide(self, state):
        return np.random.choice(4, 1, p=self._dna)
