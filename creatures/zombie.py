__author__ = 'gkour'

from config import ConfigBiology, ConfigBrain
from brains.brainsimple import RandomBrain
from creatures.human import Human
import utils
from evolution import DNA


class Zombie(Human):
    """Human like creature but with no reason, acting from the inherited fitrah or behave randomly"""

    Fitrah = [0, 0, 0, 0, 0, 0, 0]

    def __init__(self, universe, id, dna, age=0, energy=ConfigBiology.INITIAL_ENERGY, parents=None):
        super(Zombie, self).__init__(universe, id, dna, age, energy, parents)

    @staticmethod
    def get_race():
        return Zombie

    @staticmethod
    def race_name():
        return 'Zombie'

    @staticmethod
    def race_basic_dna():
        return DNA(ConfigBiology.BASE_MEMORY_SIZE,
                   ConfigBrain.BASE_LEARNING_RATE,
                   ConfigBrain.BASE_BRAIN_STRUCTURE_PARAM,
                   ConfigBiology.BASE_LEARN_FREQ,
                   ConfigBiology.BASE_LIFE_EXPECTANCY,
                   ConfigBrain.BASE_REWARD_DISCOUNT,
                   Zombie.race_fitrah())

    def decide(self, state):
        brain_actions_prob = self._brain.think(state)
        action_prob = utils.normalize_dist(brain_actions_prob) # + self.fitrah()
        decision = utils.epsilon_greedy(0, dist=action_prob)
        return decision

    def initialize_brain(self):
        self._brain = RandomBrain(self.num_actions())

    @staticmethod
    def race_fitrah():
        return utils.normalize_dist(Zombie.Fitrah)

    # @staticmethod
    # def self_race_enemy():
    #     return True

    def dying(self):
        pass

    def smarten(self):
        pass
