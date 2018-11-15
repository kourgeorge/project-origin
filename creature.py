from brain import Brain
from Config import Config
import brain_utils
import log

class Creature:
    counter = 0
    DNA_SIZE = 5
    INITIAL_ENERGY = 50

    @staticmethod
    def allocate_id():
        Creature.counter += 1
        return Creature.counter

    def __init__(self, universe, dna, id, parent):
        self._id = id
        self._energy = Creature.INITIAL_ENERGY
        self._cell = None
        self._universe = universe
        self._dna = dna
        self._brain = Brain(optimizer=Config.optimizer, s_size=Config.state_size, action_size=Config.action_size, h_size=128, scope=str(id)+'mango')
        self._age = 0

        if parent is not None:
            Config.sess.run(brain_utils.update_target_graph(str(parent)+'mango', str(id)+'mango'))

        self.obs = []
        self.acts = []
        self.rews = []

    def eat(self):
        self._universe.feed(self)

    def cell(self):
        return self._cell

    def update_cell(self, cell):
        self._cell = cell

    def coord(self):
        return self._cell.get_coord()

    def add_energy(self, amount):
        self._energy += amount

    def move(self, direction):
        self._universe.move_creature(self, direction)

    def id(self):
        return self._id

    def age(self):
        return self._age

    def mate(self):
        self._universe.mate_creature(self)

    def fight(self):
        self._universe.fight(self)

    def dna(self):
        return self._dna

    def internal_state(self):
        return [self._energy]

    def act(self):
        if self._age > 20:
            self.die()
            return

        self._age += 1
        previous_energe = self._energy
        space_state = self._universe.get_state_in_coord(self.coord())
        state = space_state + self.internal_state()
        self.obs.append(state)
        decision = self._brain.act(Config.sess, state)
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
            #self.reduce_energy(1)
            self.fight()

        self.acts.append(decision)
        self.rews.append(self.energy() - previous_energe)

        if self._age % 5 == 0:
            self._brain.train(Config.sess, self.obs, self.acts, self.rews)
            self.obs, self.acts, self.rews = [], [], []

    def energy(self):
        return self._energy

    def reduce_energy(self, amount):
        if self._energy < amount:
            self.die()
            return
        self._energy -= amount

    def die(self):
        # b_rews = (b_rews - np.mean(b_rews)) / (np.std(b_rews) + 1e-10)
        self._universe.kill(self)

    def __str__(self):
        return str(self._id)
