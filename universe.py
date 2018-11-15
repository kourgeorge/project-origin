from space import Space
from creature import Creature
from evolution import Evolution
from config import Config
import numpy as np
import utils


class Universe:

    def __init__(self):
        self._space = Space(Config.ConfigPhysics.SPACE_SIZE)
        self._time = 0
        fathers_locations = np.random.choice(Config.ConfigPhysics.SPACE_SIZE, Config.ConfigPhysics.NUM_FATHERS)
        for i in range(Config.ConfigPhysics.NUM_FATHERS):
            dna = utils.random_dna(Config.ConfigBiology.DNA_SIZE)
            self.create_creature(dna, fathers_locations[i], None)

    def space(self):
        return self._space

    def feed(self, creature):
        if creature.energy() < Config.ConfigBiology.MOVE_ENERGY:
            self.kill(creature)
            return
        creature.reduce_energy(Config.ConfigBiology.MOVE_ENERGY)
        available_food = creature.cell().get_food()
        creature.add_energy(available_food)
        creature.cell().remove_food(available_food)

    def move_creature(self, creature, direction):
        if creature.energy() < Config.ConfigBiology.MOVE_ENERGY:
            self.kill(creature)
            return
        creature.reduce_energy(Config.ConfigBiology.MOVE_ENERGY)

        current_coord = creature.coord()
        if direction == 1:
            if current_coord == Config.ConfigPhysics.SPACE_SIZE - 1:
                return
            self.space().grid()[current_coord].remove_creature(creature)
            self.space().grid()[current_coord + 1].insert_creature(creature)
        if direction == -1:
            if current_coord == 0:
                return
            self.space().grid()[current_coord].remove_creature(creature)
            self.space().grid()[current_coord - 1].insert_creature(creature)

        creature.reduce_energy(Config.ConfigBiology.MOVE_ENERGY)

    def mate_creature(self, creature):
        if creature.energy() < Config.ConfigBiology.MATE_ENERGY:
            self.kill(creature)
            return
        if creature.age() < Config.ConfigBiology.MATURITY_AGE:
            creature.reduce_energy(Config.ConfigBiology.MOVE_ENERGY)
            return

        creature.reduce_energy(Config.ConfigBiology.MATE_ENERGY)
        mate_body = creature.cell().get_mate_body(creature)
        if mate_body is None:
            return

        # Selecting the dominant parent, based on the energy level, to copy the wisdom from
        dominant_parent = creature
        if mate_body.energy() > creature.energy():
            dominant_parent = mate_body

        new_dna = Evolution.mix_dna(creature.dna(), mate_body.dna())
        self.create_creature(new_dna, creature.coord(), dominant_parent)

    def kill(self, creature):
        cell = creature.cell()
        cell.remove_creature(creature)

    def fight(self, creature):
        if creature.energy() < Config.ConfigBiology.FIGHT_ENERGY:
            self.kill(creature)
            return
        opponent = creature.cell().get_mate_body(creature)
        if opponent is None:
            return
        creature.reduce_energy(Config.ConfigBiology.FIGHT_ENERGY)
        fight_res = utils.roll_fight(creature.energy(), opponent.energy())
        if fight_res > 0:
            opponent.add_energy(creature.energy())
            # opponent.add_energy(5)
            self.kill(creature)
        else:
            creature.add_energy(opponent.energy())
            # creature.add_energy(5)
            self.kill(opponent)

    def get_state_in_coord(self, coord):
        return self.space().get_state_in_coord(coord)

    def create_creature(self, dna, coord, parent):
        descendant = Creature(universe=self, dna=dna, id=Creature.allocate_id(), parent=parent)
        self.space().grid()[coord].insert_creature(descendant)

    def pass_time(self):
        self._time += 1
        if self._time < Config.ConfigPhysics.MAX_TIME:
            for cell in self.space().grid():
                for creature in cell.creatures():
                    creature.act()
            return self._time
        else:
            return None

    def get_time(self):
        return self._time

    def give_food(self, amount):
        food_cells = np.random.choice(Config.ConfigPhysics.SPACE_SIZE, amount)
        for i in range(amount):
            self.space().grid()[food_cells[i]].add_food(1)

    def get_all_creatures(self):
        return self.space().get_all_creatures()

    def num_creatures(self):
        return len(self.get_all_creatures())
