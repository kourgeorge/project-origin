__author__ = 'gkour'

import numpy as np
from config import Config
from random import randint


class Evolution:
    @staticmethod
    def random_dna():
        vision_range = randint(1, round(Config.ConfigPhysics.SPACE_SIZE / 3))
        learning_rate = max(np.random.normal(loc=Config.ConfigBrain.LEARNING_RATE, scale=0.001), 1e-6)
        hidden_layer_size = Config.ConfigBrain.HIDDEN_LAYER_SIZE + randint(-1, +1)
        learning_frequency = max(Config.ConfigBiology.WISDOM_INTERVAL + randint(-1, 1), 1)
        max_age = max(0, Config.ConfigBiology.DYING_AGE + randint(-10, 10))
        return [vision_range, learning_rate, hidden_layer_size, learning_frequency, max_age]

    @staticmethod
    def mix_dna(dna1, dna2):
        vision_range = int(np.mean([dna1[0], dna2[0]]))
        learning_rate = max(np.random.normal(loc=np.mean([dna1[1], dna2[1]]), scale=0.001), 1e-6)
        hidden_layer_size = max(1, int(np.mean([dna1[2], dna2[2]])) + randint(-1, 1))
        learning_frequency = max(1, np.mean([dna1[3], dna2[3]]) + randint(-1, 1))
        max_age = max(0, int(np.mean([dna1[4], dna2[4]])) + randint(-1, 1))
        return [vision_range, learning_rate, hidden_layer_size, learning_frequency, max_age]
