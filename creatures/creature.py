__author__ = 'gkour'

from config import ConfigBiology, ConfigBrain
from evolution import DNA
import numpy as np
from collections import deque


class Creature:
    RACE_NAME = 'mango'

    def __init__(self, universe, id, dna, age=0, energy=ConfigBiology.INITIAL_ENERGY, parents=None):
        self._id = id
        self._name = str(id) + Creature.RACE_NAME
        self._dna = dna
        self._age = age
        self._energy = energy
        self._cell = None
        self._universe = universe
        self._parents = parents
        self._memory = deque(maxlen=self.memory_size())
        self._brain = None

        #if model_path is not None and os.path.exists(model_path):
        #    self._brain.load_model(model_path)

    #########################################################
    # Virtual function to override when creating a new race #
    #########################################################

    @staticmethod
    def race_basic_dna():
        return DNA(ConfigBiology.BASE_MEMORY_SIZE,
                   ConfigBrain.BASE_LEARNING_RATE,
                   ConfigBrain.BASE_HIDDEN_LAYER_SIZE,
                   ConfigBiology.BASE_LEARN_FREQ,
                   ConfigBiology.BASE_LIFE_EXPECTANCY,
                   ConfigBrain.BASE_GAMMA,
                   Creature.race_fitrah())

    @staticmethod
    def get_actions():
        '''return a list of actions that creature of the race can perform'''
        raise NotImplementedError()

    @staticmethod
    def self_race_enemy():
        raise NotImplementedError()

    # Identity
    @staticmethod
    def get_race():
        raise NotImplementedError()

    @staticmethod
    def race_name():
        raise NotImplementedError()

    @staticmethod
    def race_fitrah():
        raise NotImplementedError()

    def decide(self, state):
        raise NotImplementedError()

    #########################################################
    #########################################################
    #########################################################

    @staticmethod
    def vision_range():
        return 2

    def model_path(self):
        return None

    def id(self):
        return self._id

    def name(self):
        return self._name

    def age(self):
        return self._age

    def increase_age(self):
        self._age += 1

    def brain(self):
        return self._brain

    def memory_size(self):
        return self._dna.memory_size()

    def learning_rate(self):
        return self._dna.learning_rate()

    def brain_hidden_layer_size(self):
        return self._dna.hidden_layer_size()

    def learning_frequency(self):
        return self._dna.learning_frequency()

    def life_expectancy(self):
        return self._dna.life_expectancy()

    def fitrah(self):
        return self._dna.fitrah()

    def gamma(self):
        return self._dna.gamma()

    def dna(self):
        return self._dna

    def cell(self):
        return self._cell

    def get_parent(self):
        return self._parents

    def get_memory(self):
        return self._memory

    def update_cell(self, cell):
        self._cell = cell

    def coord(self):
        if self._cell is None:
            raise BaseException('An dead element should not be asked for it''s coordinate')
        return self._cell.get_coord()

    def energy(self):
        return self._energy

    def add_energy(self, amount):
        self._energy += amount

    def reduce_energy(self, amount):
        if self._energy < amount:
            raise Exception('An error - reduce energy called when there is no enough energy')
        self._energy -= amount

    def internal_state(self):
        dim_size = (2 * self.vision_range() + 1)
        energy = np.ones(shape=(dim_size, dim_size)) * self._energy
        age = np.ones(shape=(dim_size, dim_size)) * self._age
        return np.stack((energy, age))

    def get_state(self):
        space_state = self._universe.get_surroundings(self.coord(), self.vision_range())
        state = np.append(space_state, self.internal_state(), 0)
        return state

    def smarten(self):
        self._brain.train(self._memory)

    def observation_shape(self):
        food_dim = 1
        internal_state_dims = 2  # energy, age
        return [self._universe.num_races() + food_dim + internal_state_dims, 2 * self.vision_range() + 1, 2 * self.vision_range() + 1]

    def alive(self):
        return self.cell() is not None

    def add_experience(self, experience):
        self._memory.append(experience)

    def dying(self):
        """ Give a last will before dying"""
        # get smarter before dying. useful in the case of a single get_race brain
        self.smarten()
        # write the model of the last survivor.
        if self._universe.num_creatures() == 1 and self.model_path() is not None:
            self._brain.save_model(self.model_path())
            print(self.get_fitrah_dict())

    def dead_state(self):
        return np.ones(shape=self.observation_shape()) * -1

    def get_fitrah_dict(self):
        fitrah_dict = {}
        for i in range(self.num_actions()):
            fitrah_dict[str(self.get_actions()[i])] = round(self.fitrah()[i]*100)
        return fitrah_dict

    def __str__(self):
        return str(self._id)

    def num_actions(self):
        return len(self.get_actions())

    def index_to_enum(self, index):
        return self.get_actions()[index]

    def enum_to_index(self, action):
        return self.get_actions().index(action)

    def get_actions_str(self):
        return [str(action) for action in self.get_actions()]
