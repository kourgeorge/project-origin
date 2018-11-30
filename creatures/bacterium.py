from creatures.creature import Creature
from creature_actions import Actions
from config import Config
from brains.brain_dqn import BrainDQN


class Bacterium(Creature):
    _master_brain = None

    def __init__(self, universe, id, dna, age=0, energy=Config.ConfigBiology.INITIAL_ENERGY, parent=None,
                 model_path=None):
        super(Bacterium, self).__init__(universe, id, dna, age, energy, parent, model_path)
        self._brain = self.get_master_brain()

    def get_master_brain(self):
        if Bacterium._master_brain is None:
            Bacterium._master_brain = BrainDQN(lr=Config.ConfigBrain.BASE_LEARNING_RATE,
                                                       state_dims=self.state_dims(),
                                                       action_size=self.num_actions(),
                                                       h_size=Config.ConfigBrain.BASE_HIDDEN_LAYER_SIZE,
                                                       gamma=Config.ConfigBrain.BASE_GAMMA, scope='master' + self.race_name())
            return Bacterium._master_brain
        return Bacterium._master_brain

    def get_actions(self):
        return [Actions.LEFT, Actions.RIGHT, Actions.UP, Actions.DOWN, Actions.EAT, Actions.DIVIDE]

    def race_name(self):
        return 'Bacterium'

    def get_race(self):
        return Bacterium

    def decide(self, state):
        eps = max(Config.ConfigBrain.BASE_EPSILON,
                  1 - (self._age / (self.learning_frequency() * Config.ConfigBiology.MATURITY_AGE)))
        return self._brain.think(state, eps)
