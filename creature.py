from brain import Brain
import brain_utils
import log
from config import Config


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
        self._brain = Brain(lr=Config.ConfigBrain.LEARNING_RATE, s_size=Config.ConfigBrain.STATE_SIZE,
                            action_size=Config.ConfigBrain.ACTION_SIZE, h_size=Config.ConfigBrain.HIDDEN_LAYER_SIZE,
                            scope=self._name, copy_from=None if parent is None else parent.name())
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

    def dna(self):
        return self._dna

    def cell(self):
        return self._cell

    def update_cell(self, cell):
        self._cell = cell

    def coord(self):
        return self._cell.get_coord()

    def energy(self):
        return self._energy

    def add_energy(self, amount):
        self._energy += amount

    def reduce_energy(self, amount):
        if self._energy < amount:
            self.die()
            return
        self._energy -= amount

    def internal_state(self):
        return [self._energy, self._age]

    # Actions
    def act(self):
        if self._age > Config.ConfigBiology.MAX_AGE:
            self.die()
            return

        self._age += 1
        previous_energe = self._energy
        space_state = self._universe.get_state_in_coord(self.coord())
        state = space_state + self.internal_state()
        self.obs.append(state)
        decision = self._brain.act(state)
        if decision == 0:
            log.action_log[0] += 1
            self.move(-1)
        if decision == 1:
            log.action_log[1] += 1
            self.move(1)
        if decision == 2:
            log.action_log[2] += 1
            self.eat()
        if decision == 3:
            log.action_log[3] += 1
            self.mate()
        if decision == 4:
            log.action_log[4] += 1
            self.fight()

        self.acts.append(decision)
        self.rews.append(self.energy() - previous_energe)

        if self._age % Config.ConfigBiology.WISDOM_INTERVAL == 0:
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

    def die(self):
        self._universe.kill(self)

    def __str__(self):
        return str(self._id)
