__author__ = 'gkour'

from creatures.abstractcreature import AbstractCreature
from creature_actions import Actions
from config import ConfigBiology, ConfigBrain
import utils
from evolution import DNA
from brains.brainsimple import RandomBrain
import random
import numpy as np


class Human(AbstractCreature):
    Fitrah = [0, 0, 0, 0, 0, 0]

    def __init__(self, universe, id, dna, age=0, energy=ConfigBiology.INITIAL_ENERGY, parents=None):
        super(Human, self).__init__(universe, id, dna, age, energy, parents)
        self.new_born()

    @staticmethod
    def race_basic_dna():
        return DNA(ConfigBiology.BASE_MEMORY_SIZE,
                   ConfigBrain.BASE_LEARNING_RATE,
                   ConfigBrain.BASE_BRAIN_STRUCTURE_PARAM,
                   ConfigBiology.BASE_LEARN_FREQ,
                   ConfigBiology.BASE_LIFE_EXPECTANCY,
                   ConfigBrain.BASE_REWARD_DISCOUNT,
                   Human.race_fitrah())


    @staticmethod
    def get_actions():
        return [Actions.LEFT, Actions.RIGHT, Actions.UP, Actions.DOWN, Actions.EAT, Actions.FIGHT]

    @staticmethod
    def get_race():
        return Human

    @staticmethod
    def race_name():
        return 'Human'

    @staticmethod
    def race_fitrah():
        return utils.normalize_dist(Human.Fitrah)

    @staticmethod
    def self_race_enemy():
        return False

    def decide(self, state):
        eps = max(ConfigBrain.BASE_EPSILON,
                  1 - (self._age / (self.learning_frequency() * ConfigBiology.MATURITY_AGE)))
        brain_actions_prob = self.brain().think(state)
        #There is a problem with the dna fitrah (7 instead of 6).
        #action_prob = utils.normalize_dist(self.fitrah() + brain_actions_prob)
        decision = utils.epsilon_greedy(eps, brain_actions_prob)

        return decision

    def new_born(self):
        if self.get_parents() is None:
            return
        memories = [parent.get_memory() for parent in self.get_parents() if len(parent.get_memory()) > 0]
        if len(memories) == 0:
            return

        oral_tradition = np.concatenate(memories)
        self._memory.extend(
            random.sample(oral_tradition.tolist(), min(int(self.memory_size() / 2), len(oral_tradition))))
        for i in range(5):
            self.brain().train(self.get_memory())
