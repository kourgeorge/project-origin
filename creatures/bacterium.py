__author__ = 'gkour'

from creatures.abstractcreature import AbstractCreature
from creature_actions import Actions
from config import ConfigBiology, ConfigBrain
from brains.brain_dqn_tf import BrainDQN
import utils
from evolution import DNA


class Bacterium(AbstractCreature):
    _master_brain = None
    Fitrah = [0, 0, 0, 0, 1, 1]

    def __init__(self, universe, id, dna, age=0, energy=ConfigBiology.INITIAL_ENERGY, parents=None):
        super(Bacterium, self).__init__(universe, id, dna, age, energy, parents)
        self._brain = self.get_master_brain()

    def get_master_brain(self):
        if Bacterium._master_brain is None:
            Bacterium._master_brain = BrainDQN(lr=ConfigBrain.BASE_LEARNING_RATE,
                                               observation_shape=self.observation_shape(),
                                               num_actions=self.num_actions(),
                                               h_size=ConfigBrain.BASE_HIDDEN_LAYER_SIZE,
                                               gamma=ConfigBrain.BASE_GAMMA, scope='master' + self.race_name())
            return Bacterium._master_brain
        return Bacterium._master_brain

    @staticmethod
    def get_actions():
        return [Actions.LEFT, Actions.RIGHT, Actions.UP, Actions.DOWN, Actions.EAT, Actions.DIVIDE]

    @staticmethod
    def race_basic_dna():
        return DNA(ConfigBiology.BASE_MEMORY_SIZE,
                   ConfigBrain.BASE_LEARNING_RATE,
                   ConfigBrain.BASE_HIDDEN_LAYER_SIZE,
                   ConfigBiology.BASE_LEARN_FREQ,
                   ConfigBiology.BASE_LIFE_EXPECTANCY,
                   ConfigBrain.BASE_GAMMA,
                   Bacterium.race_fitrah())

    @staticmethod
    def race_name():
        return 'Bacterium'

    def get_race(self):
        return Bacterium

    @staticmethod
    def self_race_enemy():
        return True

    @staticmethod
    def race_fitrah():
        return utils.normalize_dist(Bacterium.Fitrah)

    def decide(self, state):
        eps = max(ConfigBrain.BASE_EPSILON,
                  1 - (self.age() / (self.learning_frequency() * ConfigBiology.MATURITY_AGE)))
        brain_actions_prob = self._brain.think(state)
        action_prob = utils.normalize_dist(brain_actions_prob + self.fitrah())
        action = utils.epsilon_greedy(eps, dist=action_prob)
        return action
