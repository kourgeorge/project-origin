__author__ = 'gkour'

from creatures.abstractcreature import AbstractCreature
from creature_actions import Actions
from config import ConfigBiology, ConfigBrain
import utils
from evolution import DNA
from brains.brain_simple import RandomBrain
import random
import numpy as np


class Human(AbstractCreature):
    _master_brain = None
    Fitrah = [1, 1, 1, 1, 2, 2, 2]

    def __init__(self, universe, id, dna, age=0, energy=ConfigBiology.INITIAL_ENERGY, parents=None):
        super(Human, self).__init__(universe, id, dna, age, energy, parents)
        self._brain = self.get_master_brain()
        self.new_born()

    def get_master_brain(self):
        if Human._master_brain is None:
            Human._master_brain = RandomBrain(self.num_actions())
            return Human._master_brain
        return Human._master_brain

    @staticmethod
    def race_basic_dna():
        return DNA(ConfigBiology.BASE_MEMORY_SIZE,
                   ConfigBrain.BASE_LEARNING_RATE,
                   ConfigBrain.BASE_HIDDEN_LAYER_SIZE,
                   ConfigBiology.BASE_LEARN_FREQ,
                   ConfigBiology.BASE_LIFE_EXPECTANCY,
                   ConfigBrain.BASE_REWARD_DISCOUNT,
                   Human.race_fitrah())

    @staticmethod
    def get_actions():
        return [Actions.LEFT, Actions.RIGHT, Actions.UP, Actions.DOWN, Actions.EAT, Actions.MATE, Actions.FIGHT]

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
        action_prob = utils.normalize_dist(self.fitrah() + brain_actions_prob)
        decision = utils.epsilon_greedy(eps, action_prob)
        return decision

    def new_born(self):
        if self.get_parents() is None:
            return
        oral_tradition = np.concatenate([parent.get_memory() for parent in self.get_parents()])
        self._memory.extend(random.sample(oral_tradition.tolist(), min(int(self.memory_size()/2), len(oral_tradition))))
        for i in range(5):
            self.brain().train(self.get_memory())
