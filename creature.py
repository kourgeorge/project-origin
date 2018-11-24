__author__ = 'gkour'

from brain_dqn import Brain
from config import Config


# bb = Brain(lr=Config.ConfigBrain.BASE_LEARNING_RATE, s_size=(2 * 2 + 1) * 2 + 2,
#               action_size=Config.ConfigBrain.ACTION_SIZE, h_size=8, gamma = Config.ConfigBrain.GAMMA, scope='master')


class Creature:
    counter = 0

    @staticmethod
    def allocate_id():
        Creature.counter += 1
        return Creature.counter

    def __init__(self, universe, dna, id, age=0, parent=None):
        self._id = id
        self._name = str(id) + Config.ConfigBiology.RACE_NAME
        self._dna = dna
        self._age = age
        self._energy = Config.ConfigBiology.INITIAL_ENERGY
        self._cell = None
        self._universe = universe
        parent = parent

        # surrounding(2*vision_range+1)*2(food and creatures) + 2 (internal state)
        self._state_size = (self.vision_range() * 2 + 1) * 2 + 2
        self._brain = Brain(lr=self.learning_rate(), s_size=self._state_size,
                            action_size=Config.ConfigBrain.ACTION_SIZE, h_size=self.brain_hidden_layer(),
                            scope=self._name, gamma=self.gamma(), copy_from_scope=None if parent is None else parent.name())

        # self._brain = bb
        self.obs = []
        self.acts = []
        self.rews = []
        self.newState = []

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
        return [self._energy, self._age]

    def get_state(self):
        space_state = self._universe.get_surroundings(self.coord(), self.vision_range())
        state = space_state + self.internal_state()
        return state

    # Actions
    def act(self):
        if self._age > self.max_age():
            self._universe.kill_creature(self, cause='elderly')
            return

        self._age += 1
        previous_energy = self._energy
        state = self.get_state()

        decision = self._brain.act(state)
        if decision == 0:
            self._universe.creature_move_left(self)
        if decision == 1:
            self._universe.creature_move_right(self)
        if decision == 2:
            self._universe.feed(self)
        if decision == 3:
            self._universe.creature_mate(self)
        if decision == 4:
            self._universe.creature_fight(self)
        # if decision == 5:
        #     log.action_log[5] += 1
        #     self.smarten()
        self.obs.append(state)
        self.acts.append(decision)
        self.rews.append(self.energy() - previous_energy)

        if self.alive():
            self.newState.append(self.get_state())
        else:
            self.newState.append([-1] * self.state_size())
            self.smarten()

        if self._age % self.learning_frequency() == 0:
            self.smarten()

    def smarten(self):
        self._brain.train(self.obs, self.acts, self.rews, self.newState)
        self.obs, self.acts, self.rews, self.newState = [], [], [], []

    def state_size(self):
        return self._state_size

    def alive(self):
        return self.cell() is not None

    def __str__(self):
        return str(self._id)
