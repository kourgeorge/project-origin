__author__ = 'gkour'

import numpy as np
from random import randint
import utils
from config import Config


class Evolution:

    @staticmethod
    def get_Basic_dna(num_actions):
        return DNA(Config.ConfigBiology.MEMORY_SIZE,
                   Config.ConfigBrain.BASE_LEARNING_RATE,
                   Config.ConfigBrain.BASE_HIDDEN_LAYER_SIZE,
                   Config.ConfigBiology.BASE_LEARN_FREQ,
                   Config.ConfigBiology.BASE_LIFE_EXPECTANCY,
                   Config.ConfigBrain.BASE_GAMMA,
                   utils.softmax(np.ones(num_actions)))

    @staticmethod
    def mix_dna(dna1, dna2):
        new_dna = DNA(np.mean([dna1.memory_size(), dna2.memory_size()]),
                      np.mean([dna1.learning_rate(), dna2.learning_rate()]),
                      np.mean([dna1.hidden_layer_size(), dna2.hidden_layer_size()]),
                      np.mean([dna1.learning_frequency(), dna2.learning_frequency()]),
                      np.mean([dna1.life_expectancy(), dna2.life_expectancy()]),
                      np.mean([dna1.gamma(), dna2.gamma()]),
                      np.mean([dna1.action_bias(), dna2.action_bias()]))
        return Evolution.mutate_dna(new_dna)

    @staticmethod
    def mutate_dna(dna):
        memory_size = max(10, int(dna.memory_size()) + randint(-1, 1))
        learning_rate = max(np.random.normal(loc=dna.learning_rate(), scale=0.001), 1e-6)
        hidden_layer_size = max(2, dna.hidden_layer_size() + randint(-1, +1))
        learning_frequency = max(dna.learning_frequency() + randint(-1, 1), 1)
        life_expectancy = max(0, dna.life_expectancy() + randint(-10, 10))
        gamma = max(0.1, min(1, np.random.normal(loc=dna.gamma(), scale=0.001)))
        action_bias = utils.softmax(dna.action_bias() + np.random.normal(loc=0, scale=0.001, size=dna.action_bias().size))
        return DNA(memory_size, learning_rate, hidden_layer_size, learning_frequency, life_expectancy, gamma, action_bias)


class DNA:
    def __init__(self, base_memory_size,
                 base_learning_rate,
                 base_hidden_layer,
                 base_learning_frequency,
                 base_life_expectancy,
                 base_gamma,
                 base_action_bias):
        self._memory_size = base_memory_size
        self._learning_rate = base_learning_rate
        self._hidden_layer_size = base_hidden_layer
        self._learning_frequency = base_learning_frequency
        self._life_expectancy = base_life_expectancy
        self._gamma = base_gamma
        self._action_bias = base_action_bias

    def memory_size(self):
        return self._memory_size

    def learning_rate(self):
        return self._learning_rate

    def learning_frequency(self):
        return self._learning_frequency

    def hidden_layer_size(self):
        return self._hidden_layer_size

    def life_expectancy(self):
        return self._life_expectancy

    def gamma(self):
        return self._gamma

    def action_bias(self):
        return self._action_bias

