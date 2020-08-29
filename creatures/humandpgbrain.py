__author__ = 'gkour'

from config import ConfigBiology, ConfigBrain
from brains.braindqntorch import BrainDQN
from brains.brainpg import BrainPG
import utils
from creatures.human import Human
from evolution import DNA
from creature_actions import Actions
import os


class HumanPGBrain(Human):
    Fitrah = [0, 0, 0, 0, 0, 0]

    def __init__(self, universe, id, dna, age=0, energy=ConfigBiology.INITIAL_ENERGY, parents=None):
        super(HumanPGBrain, self).__init__(universe, id, dna, age, energy, parents)

    @staticmethod
    def get_race():
        return HumanPGBrain

    @staticmethod
    def race_name():
        return 'HumanTorchBrain'

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
        self._brain = BrainDQN(observation_shape=tuple(self.observation_shape()),
                               num_actions=self.num_actions(), reward_discount=self.reward_discount())


class HumanTorchUnifiedBrain(HumanPGBrain):
    _master_brain = None

    def __init__(self, universe, id, dna, age=0, energy=ConfigBiology.INITIAL_ENERGY, parents=None):
        super(HumanTorchUnifiedBrain, self).__init__(universe, id, dna, age, energy, parents)

    def initialize_brain(self):
        self._brain = self.get_master_brain()

    def get_master_brain(self):
        if HumanTorchUnifiedBrain._master_brain is None:
            HumanTorchUnifiedBrain._master_brain = BrainPG(observation_shape=tuple(self.observation_shape()),
                                                            num_actions=self.num_actions(),
                                                            reward_discount=ConfigBrain.BASE_REWARD_DISCOUNT)
            if self.model_path() is not None and os.path.exists(self.model_path()):
                HumanTorchUnifiedBrain._master_brain.load_model(self.model_path())
        return HumanTorchUnifiedBrain._master_brain

    @staticmethod
    def get_race():
        return HumanTorchUnifiedBrain

    @staticmethod
    def race_name():
        return 'HumanPGUnifiedBrain'

    def new_born(self):
        pass
