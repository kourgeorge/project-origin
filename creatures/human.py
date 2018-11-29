from creatures.creature import Creature
from creature_actions import Actions
from config import Config
from brains.brain_dqn import BrainDQN


class Human(Creature):
    _master_brain = None

    def __init__(self, universe, id, dna, age=0, energy=Config.ConfigBiology.INITIAL_ENERGY, parent=None,
                 model_path=None):
        super(Human, self).__init__(universe, id, dna, age, energy, parent, model_path)
        self._brain = self.get_master_brain()

    def get_master_brain(self):
        if Human._master_brain is None:
            Human._master_brain = BrainDQN(lr=Config.ConfigBrain.BASE_LEARNING_RATE,
                                                   state_dims=(4, 2 * Config.ConfigBiology.BASE_VISION_RANGE + 1,
                                                    2 * Config.ConfigBiology.BASE_VISION_RANGE + 1),
                                                   action_size=self.num_actions(),
                                                   h_size=Config.ConfigBrain.BASE_HIDDEN_LAYER_SIZE,
                                                   gamma=Config.ConfigBrain.BASE_GAMMA,
                                                   scope='master' + self.race_name())
            return Human._master_brain
        return Human._master_brain

    def get_actions(self):
        return [Actions.LEFT, Actions.RIGHT, Actions.UP, Actions.DOWN, Actions.EAT, Actions.MATE, Actions.WORK]

    def race(self):
        return Human

    def race_name(self):
        return 'Human'

    def decide(self, state):
        eps = max(Config.ConfigBrain.EPSILON,
                  1 - (self._age / (self.learning_frequency() * Config.ConfigBiology.MATURITY_AGE)))
        return self._brain.think(state, eps)
