__author__ = 'gkour'

from config import ConfigBiology, ConfigBrain
from brains.brain_dqn import BrainDQN
import utils
from creatures.human import Human
from evolution import DNA


class HumanDQNBrain(Human):
    _master_brain = None
    Fitrah = [0, 0, 0, 0, 0, 0, 0]

    def __init__(self, universe, id, dna, age=0, energy=ConfigBiology.INITIAL_ENERGY, parents=None):
        super(HumanDQNBrain, self).__init__(universe, id, dna, age, energy, parents)
        self._brain = BrainDQN(observation_shape=self.observation_shape(),
                               num_actions=self.num_actions(), lr=ConfigBrain.BASE_LEARNING_RATE,
                               h_size=ConfigBrain.BASE_HIDDEN_LAYER_SIZE, scope=str(id) + self.race_name(),
                               gamma=ConfigBrain.BASE_GAMMA)
        # self.new_born()

    def get_master_brain(self):
        if HumanDQNBrain._master_brain is None:
            HumanDQNBrain._master_brain = BrainDQN(observation_shape=self.observation_shape(),
                                                   num_actions=self.num_actions(), lr=ConfigBrain.BASE_LEARNING_RATE,
                                                   h_size=ConfigBrain.BASE_HIDDEN_LAYER_SIZE, scope=self.race_name(),
                                                   gamma=ConfigBrain.BASE_GAMMA)
            return HumanDQNBrain._master_brain
        return HumanDQNBrain._master_brain

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
                   ConfigBrain.BASE_HIDDEN_LAYER_SIZE,
                   ConfigBiology.BASE_LEARN_FREQ,
                   ConfigBiology.BASE_LIFE_EXPECTANCY,
                   ConfigBrain.BASE_GAMMA,
                   HumanDQNBrain.race_fitrah())

    @staticmethod
    def race_fitrah():
        return utils.normalize_dist(HumanDQNBrain.Fitrah)

    @staticmethod
    def self_race_enemy():
        return False

    def model_path(self):
        return './models/' + self.race_name()
