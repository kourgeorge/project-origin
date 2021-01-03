__author__ = 'gkour'

import os

import torch
from torch.distributions import Categorical

import utils
from brains.brainpg import BrainPG
from config import ConfigBiology, ConfigBrain
from creatures.human import Human
from evolution import DNA


class HumanPGBrain(Human):
    Fitrah = [0, 0, 0, 0, 0]

    def __init__(self, universe, id, dna, age=0, energy=ConfigBiology.INITIAL_ENERGY, parents=None):
        super(HumanPGBrain, self).__init__(universe, id, dna, age, energy, parents)

    @staticmethod
    def get_race():
        return HumanPGBrain

    @staticmethod
    def race_name():
        return 'HumanPGBrain'

    @staticmethod
    def race_basic_dna():
        return DNA(ConfigBiology.BASE_MEMORY_SIZE,
                   ConfigBrain.BASE_LEARNING_RATE,
                   ConfigBrain.BASE_BRAIN_STRUCTURE_PARAM,
                   ConfigBiology.BASE_LEARN_FREQ,
                   ConfigBiology.BASE_LIFE_EXPECTANCY,
                   ConfigBrain.BASE_REWARD_DISCOUNT,
                   HumanPGBrain.race_fitrah())

    @staticmethod
    def race_fitrah():
        return utils.normalize_dist(HumanPGBrain.Fitrah)

    # @staticmethod
    # def self_race_enemy():
    #     return True

    def initialize_brain(self):
        self._brain = BrainPG(observation_shape=tuple(self.observation_shape()),
                              num_actions=self.num_actions(), reward_discount=self.reward_discount())

    def decide(self, state):
        eps = max(ConfigBrain.BASE_EPSILON,
                  1 - (self._age / (self.learning_frequency() * ConfigBiology.MATURITY_AGE)))
        brain_actions_prob = self.brain().think(state)
        # action_prob = utils.normalize_dist(self.fitrah() + brain_actions_prob)
        # decision = utils.dist_selection(brain_actions_prob)
        decision = Categorical(probs=torch.tensor(brain_actions_prob)).sample().item()
        return decision


class HumanPGUnifiedBrain(HumanPGBrain):
    _master_brain = None

    def __init__(self, universe, id, dna, age=0, energy=ConfigBiology.INITIAL_ENERGY, parents=None):
        super(HumanPGUnifiedBrain, self).__init__(universe, id, dna, age, energy, parents)

    def initialize_brain(self):
        self._brain = self.get_master_brain()

    def get_master_brain(self):
        if HumanPGUnifiedBrain._master_brain is None:
            HumanPGUnifiedBrain._master_brain = BrainPG(observation_shape=tuple(self.observation_shape()),
                                                        num_actions=self.num_actions(),
                                                        reward_discount=ConfigBrain.BASE_REWARD_DISCOUNT,
                                                        learning_rate=ConfigBrain.BASE_LEARNING_RATE)
            if self.model_path() is not None and os.path.exists(self.model_path()):
                HumanPGUnifiedBrain._master_brain.load_model(self.model_path())
        return HumanPGUnifiedBrain._master_brain

    @staticmethod
    def get_race():
        return HumanPGUnifiedBrain

    @staticmethod
    def race_name():
        return 'HumanPGUnifiedBrain'

    def new_born(self):
        pass
    #
    # def get_state(self):
    #     state = super().get_state()
    #     return state[0,:,:]
