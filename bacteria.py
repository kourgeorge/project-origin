from creature import Creature
from creature_actions import Actions
from config import Config
from brain_dqn import Brain


class Bacteria(Creature):
    _master_brain = None

    def __init__(self, universe, id, dna, age=0, energy=Config.ConfigBiology.INITIAL_ENERGY, parent=None,
                 model_path=None):
        super(Bacteria, self).__init__(universe, id, dna, age, energy, parent, model_path)
        self._brain = self.get_master_brain()

    def get_master_brain(self):
        if Bacteria._master_brain is None:
            Bacteria._master_brain = Brain(lr=Config.ConfigBrain.BASE_LEARNING_RATE,
                                           state_dims=(4, 2 * Config.ConfigBiology.BASE_VISION_RANGE + 1,
                                                       2 * Config.ConfigBiology.BASE_VISION_RANGE + 1),
                                           action_size=self.num_actions(),
                                           h_size=Config.ConfigBrain.BASE_HIDDEN_LAYER_SIZE,
                                           gamma=Config.ConfigBrain.BASE_GAMMA, scope='master' + self.race_name())
            return Bacteria._master_brain
        return Bacteria._master_brain

    def get_actions(self):
        return [Actions.LEFT, Actions.RIGHT, Actions.UP, Actions.DOWN, Actions.EAT, Actions.DIVIDE]

    def race_name(self):
        return 'Bacteria'

    def race(self):
        return Bacteria
