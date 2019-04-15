__author__ = 'gkour'

from config import ConfigBiology, ConfigBrain
from brains.braindqntorch import BrainDQN
import utils
from creatures.human import Human
from evolution import DNA
from creature_actions import Actions
import os


class HumanTorchBrain(Human):
    _master_brain = None
    Fitrah = [0, 0, 0, 0, 0, 0, 0]

    def __init__(self, universe, id, dna, age=0, energy=ConfigBiology.INITIAL_ENERGY, parents=None):
        super(HumanTorchBrain, self).__init__(universe, id, dna, age, energy, parents)
        #self._brain = self.get_master_brain()
        self._brain = BrainDQN(observation_shape=tuple(self.observation_shape()),
                             num_actions=self.num_actions(), reward_discount=self.reward_discount())

    def get_master_brain(self):
        if HumanTorchBrain._master_brain is None:
            HumanTorchBrain._master_brain = BrainDQN(observation_shape=tuple(self.observation_shape()),
                                                     num_actions=self.num_actions(), reward_discount=ConfigBrain.BASE_REWARD_DISCOUNT)
            if self.model_path() is not None and os.path.exists(self.model_path()):
                HumanTorchBrain._master_brain.load_model(self.model_path())
            return HumanTorchBrain._master_brain
        return HumanTorchBrain._master_brain

    @staticmethod
    def get_race():
        return HumanTorchBrain

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
                   HumanTorchBrain.race_fitrah())

    @staticmethod
    def race_fitrah():
        return utils.normalize_dist(HumanTorchBrain.Fitrah)

    @staticmethod
    def self_race_enemy():
        return False

    # def new_born(self):
    #     pass

class HumanTorchBrain2(HumanTorchBrain):
    def __init__(self, universe, id, dna, age=0, energy=ConfigBiology.INITIAL_ENERGY, parents=None):
        super(HumanTorchBrain2, self).__init__(universe, id, dna, age, energy, parents)

    @staticmethod
    def get_race():
        return HumanTorchBrain2

    @staticmethod
    def race_name():
        return 'HumanDQNBrain2'
