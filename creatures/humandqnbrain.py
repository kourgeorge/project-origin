__author__ = 'gkour'

from config import ConfigBiology, ConfigBrain
from brains.braindqn import BrainDQN
import utils
from creatures.human import Human
from evolution import DNA


class HumanDQNBrain(Human):
    Fitrah = [0, 0, 0, 0, 0, 0, 0]

    def __init__(self, universe, id, dna, age=0, energy=ConfigBiology.INITIAL_ENERGY, parents=None):
        super(HumanDQNBrain, self).__init__(universe, id, dna, age, energy, parents)

    def initialize_brain(self):
        self._brain = BrainDQN(observation_shape=self.observation_shape(),
                               num_actions=self.num_actions(),
                               reward_discount=self.reward_discount())



    @staticmethod
    def get_race():
        return HumanDQNBrain

    @staticmethod
    def race_name():
        return 'HumanDQNBrain'

    @staticmethod
    def race_basic_dna():
        return DNA(ConfigBiology.BASE_MEMORY_SIZE,
                   ConfigBrain.BASE_LEARNING_RATE,
                   ConfigBrain.BASE_BRAIN_STRUCTURE_PARAM,
                   ConfigBiology.BASE_LEARN_FREQ,
                   ConfigBiology.BASE_LIFE_EXPECTANCY,
                   ConfigBrain.BASE_REWARD_DISCOUNT,
                   HumanDQNBrain.race_fitrah())

    @staticmethod
    def race_fitrah():
        return utils.normalize_dist(HumanDQNBrain.Fitrah)

    @staticmethod
    def self_race_enemy():
        return False

    def model_path(self):
        return './models/' + self.race_name()

    def new_born(self):
        pass
