__author__ = 'gkour'

from space import Space
from creature import Creature
from evolution import Evolution
from config import Config
import numpy as np
import utils
from stats import Stats

FOOD_CREATURE_RATIO = 0.5


class Universe:

    def __init__(self):
        self._space = Space(Config.ConfigPhysics.SPACE_SIZE)
        self._time = 0
        fathers_locations = np.random.choice(Config.ConfigPhysics.SPACE_SIZE, Config.ConfigPhysics.NUM_FATHERS)
        for i in range(Config.ConfigPhysics.NUM_FATHERS):
            dna = Evolution.random_dna()
            self.create_creature(dna, fathers_locations[i], None)

    # Space Management
    def space(self):
        return self._space

    def get_surroundings(self, coord, vision_range):
        return self._space.get_state_in_coord(coord, vision_range)

    # Time Management
    def pass_time(self):
        self._time += 1
        if self._time < Config.ConfigPhysics.ETERNITY and self.num_creatures() > 0:
            self.give_food(round(self.num_creatures() * FOOD_CREATURE_RATIO))
            for creature in self.get_all_creatures():
                if creature.alive():
                    creature.act()
            return self._time
        else:
            return None

    def get_time(self):
        return self._time

    # Food Supply management
    def give_food(self, amount):
        food_cells = np.random.choice(Config.ConfigPhysics.SPACE_SIZE, amount)
        for i in range(amount):
            self.space().grid()[food_cells[i]].add_food(1)

    # Creatures Control
    def create_creature(self, dna, coord, parent):
        descendant = Creature(universe=self, dna=dna, id=Creature.allocate_id(), parent=parent)
        cell = self.space().grid()[coord].insert_creature(descendant)
        descendant.update_cell(cell)

    def get_all_creatures(self):
        return self.space().get_all_creatures()

    def get_food_distribution(self):
        return self.space().get_food_distribution()

    def get_creatures_distribution(self):
        return self.space().get_creatures_distribution()

    def num_creatures(self):
        return len(self.get_all_creatures())

    def feed(self, creature):
        if creature.energy() < Config.ConfigBiology.MOVE_ENERGY:
            self.kill(creature)
            return
        creature.reduce_energy(Config.ConfigBiology.MOVE_ENERGY)
        available_food = creature.cell().get_food()
        meal = min(5, available_food)
        creature.add_energy(meal)
        creature.cell().remove_food(meal)

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
            new_cell = self.space().grid()[current_coord + 1].insert_creature(creature)
            creature.update_cell(new_cell)
        if direction == -1:
            if current_coord == 0:
                return
            self.space().grid()[current_coord].remove_creature(creature)
            new_cell = self.space().grid()[current_coord - 1].insert_creature(creature)
            creature.update_cell(new_cell)

    def mate_creature(self, creature):
        if creature.age() < Config.ConfigBiology.MATURITY_AGE:
            if creature.energy() < Config.ConfigBiology.MOVE_ENERGY:
                self.kill(creature)
                return
            creature.reduce_energy(Config.ConfigBiology.MOVE_ENERGY)
            return

        if creature.energy() < Config.ConfigBiology.MATE_ENERGY:
            self.kill(creature)
            return

        creature.reduce_energy(Config.ConfigBiology.MATE_ENERGY)
        mate_body = creature.cell().find_nearby_creature(creature)
        if mate_body is None:
            return

        # Selecting the dominant parent, based on the energy level, to copy the wisdom from
        dominant_parent = creature
        if mate_body.energy() > creature.energy():
            dominant_parent = mate_body

        new_dna = Evolution.mix_dna(creature.dna(), mate_body.dna())
        self.create_creature(new_dna, creature.coord(), dominant_parent)

    def kill(self, creature, cause='fatigue'):
        creature.reduce_energy(creature.energy())
        cell = creature.cell()
        creature.update_cell(None)
        cell.remove_creature(creature)
        if cause == 'fatigue':
            Stats.death_cause[0] += 1
        if cause == 'fight':
            Stats.death_cause[1] += 1
        if cause == 'elderly':
            Stats.death_cause[2] += 1

    def fight(self, creature):
        if creature.energy() < Config.ConfigBiology.FIGHT_ENERGY:
            self.kill(creature, 'fight')
            return
        creature.reduce_energy(Config.ConfigBiology.FIGHT_ENERGY)

        # if creature.energy() < Config.ConfigBiology.FIGHT_ENERGY:
        #     self.kill(creature, 'fight')
        #     return
        # creature.reduce_energy(Config.ConfigBiology.FIGHT_ENERGY)
        # opponent = creature.cell().find_nearby_creature(creature)
        # if opponent is None:
        #     return
        # fight_res = utils.roll_fight(creature.energy(), opponent.energy())
        # if fight_res > 0:
        #     opponent.add_energy(creature.energy())
        #     # opponent.add_energy(5)
        #     self.kill(creature, 'fight')
        # else:
        #     creature.add_energy(opponent.energy())
        #     # creature.add_energy(5)
        #     self.kill(opponent, 'fight')

    @staticmethod
    def get_creatures_counter():
        return Creature.counter
