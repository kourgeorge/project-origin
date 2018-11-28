__author__ = 'gkour'

from brain_dqn import Brain
from config import Config
from creature_actions import Actions
import os
import numpy as np

master_brain = Brain(lr=Config.ConfigBrain.BASE_LEARNING_RATE,
                     state_dims=(4, 2*Config.ConfigBiology.BASE_VISION_RANGE+1, 2*Config.ConfigBiology.BASE_VISION_RANGE+1),
                     action_size=Actions.num_actions(), h_size=Config.ConfigBrain.BASE_HIDDEN_LAYER_SIZE,
                     gamma=Config.ConfigBrain.BASE_GAMMA, scope='master')


class Creature:
    counter = 0

    @staticmethod
    def allocate_id():
        Creature.counter += 1
        return Creature.counter

    def __init__(self, universe, dna, id, age=0, energy=Config.ConfigBiology.INITIAL_ENERGY, parent=None,
                 model_path=None):
        self._id = id
        self._name = str(id) + Config.ConfigBiology.RACE_NAME
        self._dna = dna
        self._age = age
        self._energy = energy
        self._cell = None
        self._universe = universe
        parent = parent
        self._model_path = model_path

        # self._brain = Brain(lr=self.learning_rate(), s_size=self.surroundings_size(),
        #                     action_size=Actions.num_actions(), h_size=self.brain_hidden_layer(),
        #                     scope=self._name, gamma=self.gamma(), copy_from_scope=None if parent is None else parent.name())

        self._brain = master_brain
        self.obs = []
        self.acts = []
        self.rews = []
        self.newState = []

        if model_path is not None and os.path.exists(model_path):
            self._brain.load_model(model_path)

    # Identity
    def id(self):
        return self._id

    def name(self):
        return self._name

    def age(self):
        return self._age

    def brain(self):
        return self._brain

    def vision_range(self):
        return self._dna[0]

    def learning_rate(self):
        return self._dna[1]

    def brain_hidden_layer(self):
        return self._dna[2]

    def learning_frequency(self):
        return self._dna[3]

    def max_age(self):
        return self._dna[4]

    def gamma(self):
        return self._dna[5]

    def dna(self):
        return self._dna

    def cell(self):
        return self._cell

    def update_cell(self, cell):
        self._cell = cell

    def coord(self):
        if self._cell is None:
            print(self)
        return self._cell.get_coord()

    def energy(self):
        return self._energy

    def add_energy(self, amount):
        self._energy += amount

    def reduce_energy(self, amount):
        if self._energy < amount:
            print('An error - reduce energy called when there is no enough energy')
            return
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

    # Actions
    def act(self):
        if self._age > self.max_age():
            self._universe.kill_creature(self, cause='elderly')
            return

        self._age += 1
        previous_energy = self._energy
        state = self.get_state()

        eps = max(Config.ConfigBrain.EPSILON, 1-(self._age/Config.ConfigBiology.MATURITY_AGE))
        decision = self._brain.act(state, eps)
        action = Actions.index_to_enum(decision)
        if action == Actions.LEFT:
            self._universe.creature_move_left(self)
        if action == Actions.RIGHT:
            self._universe.creature_move_right(self)
        if action == Actions.UP:
            self._universe.creature_move_up(self)
        if action == Actions.DOWN:
            self._universe.creature_move_down(self)
        if action == Actions.EAT:
            self._universe.creature_eat(self)
        if action == Actions.MATE:
            self._universe.creature_mate(self)
        if action == Actions.FIGHT:
            self._universe.creature_fight(self)
        if action == Actions.WORK:
            self._universe.creature_work(self)
        if action == Actions.DEVIDE:
            self._universe.creature_divide(self)
        # if decision == 6:
        #     log.action_log[6] += 1
        #     self.smarten()
        self.obs.append(state)
        self.acts.append(decision)
        self.rews.append(self.energy() - previous_energy)

        if self.alive():
            self.newState.append(self.get_state())
        else:
            self.newState.append(self._dead_state() * self.surroundings_size())
            self.smarten()

        if self._age % self.learning_frequency() == 0:
            self.smarten()

    def smarten(self):
        self._brain.train(self.obs, self.acts, self.rews, self.newState)
        self.obs, self.acts, self.rews, self.newState = [], [], [], []

    def surroundings_size(self):
        # surrounding(2*vision_range+1)*2(food and creatures) + 2 (internal state)
        return (2 * self.vision_range() + 1) ** 2

    def state_dims(self):
        # Creatures, Food, Eergy, age
        return (4, 2 * self.vision_range() + 1, 2 * self.vision_range() + 1)

    def alive(self):
        return self.cell() is not None

    def die(self):
        # write the model of the last survivor.
        if self._universe.num_creatures == 1 and self._model_path is not None:
            self._brain.save_model(self._model_path)

    def _dead_state(self):
        return np.ones(shape=self.state_dims())*-1

    def __str__(self):
        return str(self._id)
