from creatures.creature import Creature
from creature_actions import Actions
from config import Config
from brains.brain_dqn import BrainDQN
import utils


class Human(Creature):
    _master_brain = None
    Fitrah = [0.1, 0.1, 0.1, 0.1, 0.2, 0.2]

    def __init__(self, universe, id, dna, age=0, energy=Config.ConfigBiology.INITIAL_ENERGY, parents=None,
                 model_path=None):
        super(Human, self).__init__(universe, id, dna, age, energy, parents, model_path)
        self._brain = self.get_master_brain()
        # self.new_born()

    def get_master_brain(self):
        if Human._master_brain is None:
            Human._master_brain = BrainDQN(lr=Config.ConfigBrain.BASE_LEARNING_RATE,
                                           state_dims=self.state_dims(),
                                           action_size=self.num_actions(),
                                           h_size=Config.ConfigBrain.BASE_HIDDEN_LAYER_SIZE,
                                           gamma=Config.ConfigBrain.BASE_GAMMA,
                                           scope='master' + self.race_name())
            return Human._master_brain
        return Human._master_brain

    @staticmethod
    def get_actions():
        return [Actions.LEFT, Actions.RIGHT, Actions.UP, Actions.DOWN, Actions.EAT, Actions.MATE]

    @staticmethod
    def get_race():
        return Human

    @staticmethod
    def race_name():
        return 'Human'

    @staticmethod
    def race_fitrah():
        return utils.softmax(Human.Fitrah, len(Human.get_actions()))

    @staticmethod
    def self_race_enemy():
        return False

    def decide(self, state):
        eps = max(Config.ConfigBrain.BASE_EPSILON,
                 1 - (self._age / (self.learning_frequency() * Config.ConfigBiology.MATURITY_AGE)))
        brain_actions_prob = self._brain.think(state)
        action_prob = utils.softmax(brain_actions_prob, temprature=len(self.fitrah()))
        decision = utils.epsilon_greedy(eps, action_prob)
        print(self.fitrah())
        return decision

    def new_born(self):
        if self.get_parent() is None:
            return
        self._memory = self.get_parent().get_memory()
