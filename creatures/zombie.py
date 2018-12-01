from config import Config
from brains.brain_simple import RandomBrain
from creatures.human import Human
import utils


class Zombie(Human):
    Fitrah = [0, 0, 0, 0, 0, 0]

    def __init__(self, universe, id, dna, age=0, energy=Config.ConfigBiology.INITIAL_ENERGY, parents=None,
                 model_path=None):
        super(Zombie, self).__init__(universe, id, dna, age, energy, parents, model_path)
        self._brain = RandomBrain(self.num_actions())

    @staticmethod
    def get_race():
        return Zombie

    @staticmethod
    def race_name():
        return 'Zombie'

    def decide(self, state):
        brain_actions_prob = self._brain.think(state)
        #action_prob = utils.softmax(brain_actions_prob + self.fitrah())
        decision = utils.epsilon_greedy(0, dist=brain_actions_prob)
        return decision

    @staticmethod
    def self_race_enemy():
        return True

    def dying(self):
        pass

    def smarten(self):
        pass