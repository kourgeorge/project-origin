__author__ = 'gkour'

from brain import Brain
import datacollector
from config import Config
import utils


class Creature:
    counter = 0

    @staticmethod
    def allocate_id():
        Creature.counter += 1
        return Creature.counter

    def __init__(self, universe, dna, id, parent):
        self._id = id
        self._name = str(id) + Config.ConfigBiology.RACE_NAME
        self._dna = dna
        self._age = 0
        self._energy = Config.ConfigBiology.INITIAL_ENERGY
        self._cell = None
        self._universe = universe
        parent = None
        self.completed_action_in_current_cycle = False

        # sorounding(2*vrange+1)*2(food and creatures) + 2 (intenal state)
        state_size = (self.vision_range()*2 + 1) * 2 + 2
        self._brain = Brain(lr=self.learning_rate(), s_size=state_size,
                            action_size=Config.ConfigBrain.ACTION_SIZE, h_size=self.brain_hidden_layer(),
                            scope=self._name, copy_from_scope=None if parent is None else parent.name())
        self.obs = []
        self.acts = []
        self.rews = []

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

    # Actions
    def act(self):
        if self._age > self.max_age():
            self._universe.kill(self, cause='elderly')
            return

        self._age += 1
        previous_energy = self._energy
        space_state = self._universe.get_surroundings(self.coord(), self.vision_range())
        state = space_state + self.internal_state()
        self.obs.append(state)
        decision = self._brain.act(state)
        if decision == 0:
            datacollector.action_log[0] += 1
            self.move(-1)
        if decision == 1:
            datacollector.action_log[1] += 1
            self.move(1)
        if decision == 2:
            datacollector.action_log[2] += 1
            self.eat()
        if decision == 3:
            datacollector.action_log[3] += 1
            self.mate()
        if decision == 4:
            datacollector.action_log[4] += 1
            self.fight()
        # if decision == 5:
        #     log.action_log[5] += 1
        #     self.smarten()

        self.acts.append(decision)
        self.rews.append(self.energy() - previous_energy)

        if self._age % self.learning_frequency() == 0:
            self.smarten()

    def move(self, direction):
        self._universe.move_creature(self, direction)

    def eat(self):
        self._universe.feed(self)

    def mate(self):
        self._universe.mate_creature(self)

    def fight(self):
        self._universe.fight(self)

    def smarten(self):
        self._brain.train(self.obs, self.acts, self.rews)
        self.obs, self.acts, self.rews = [], [], []

    def alive(self):
        return self.cell() is not None

    def __str__(self):
        return str(self._id)
