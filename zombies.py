from creature import Creature
from creature_actions import Actions
from config import Config
from simple_brains import RandomBrain
from human import Human


class Zombie(Human):

    def __init__(self, universe, id, dna, age=0, energy=Config.ConfigBiology.INITIAL_ENERGY, parent=None,
                 model_path=None):
        super(Zombie, self).__init__(universe, id, dna, age, energy, parent, model_path)
        self._brain = RandomBrain(self.num_actions())

    def race(self):
        return Zombie

    def race_name(self):
        return 'Zombie'

    def decide(self, state):
        return self._brain.decide_on_action(state)
