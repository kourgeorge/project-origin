__author__ = 'gkour'

from space import Space
from creature import Creature
from evolution import Evolution
from config import Config
import numpy as np
import utils
from creature_actions import Actions


class Universe:

    def __init__(self, statistics=None):
        self._space = Space(Config.ConfigPhysics.SPACE_SIZE)
        self._time = 0
        fathers_locations = np.random.choice(Config.ConfigPhysics.SPACE_SIZE, Config.ConfigPhysics.NUM_FATHERS)
        for i in range(Config.ConfigPhysics.NUM_FATHERS):
            dna = Evolution.random_dna()
            self.create_creature(dna=dna, coord=fathers_locations[i], age=Config.ConfigBiology.MATURITY_AGE, parent=None)
        self.statistics = statistics

    # Space Management
    def space(self):
        return self._space

    def get_surroundings(self, coord, vision_range):
        return self._space.get_state_in_coord(coord, vision_range)

    # Time Management
    def pass_time(self):
        self._time += 1
        if self._time < Config.ConfigPhysics.ETERNITY and self.num_creatures() > 0:
            self.give_food(round(self.num_creatures() * Config.ConfigPhysics.FOOD_CREATURE_RATIO))
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
    def create_creature(self, dna, coord, age=0, energy=Config.ConfigBiology.INITIAL_ENERGY, parent=None):
        descendant = Creature(universe=self, dna=dna, id=Creature.allocate_id(), age=age, energy=energy, parent=parent)
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
        self.statistics.action_dist[2] += 1
        if creature.energy() < Config.ConfigBiology.MOVE_ENERGY:
            self.kill_creature(creature)
            return
        creature.reduce_energy(Config.ConfigBiology.MOVE_ENERGY)
        available_food = creature.cell().get_food()
        meal = min(Config.ConfigBiology.MEAL_SIZE, available_food)
        creature.add_energy(meal)
        creature.cell().remove_food(meal)

    def creature_move_left(self, creature):
        self.statistics.action_dist[Actions.get_available_action_indx(Actions.LEFT)] += 1
        self.move_creature(creature, -1)

    def creature_move_right(self, creature):
        self.statistics.action_dist[Actions.get_available_action_indx(Actions.RIGHT)] += 1
        self.move_creature(creature, 1)

    def move_creature(self, creature, direction):
        if creature.energy() < Config.ConfigBiology.MOVE_ENERGY:
            self.kill_creature(creature)
            return
        creature.reduce_energy(Config.ConfigBiology.MOVE_ENERGY)

        current_coord = creature.coord()
        if direction == 1:
            if current_coord == Config.ConfigPhysics.SPACE_SIZE - 1:
                self.kill_creature(creature) #Slippery edges physics
                return
            self.space().grid()[current_coord].remove_creature(creature)
            new_cell = self.space().grid()[current_coord + 1].insert_creature(creature)
            creature.update_cell(new_cell)
        if direction == -1:
            if current_coord == 0:
                self.kill_creature(creature) #Slippery edges physics
                return
            self.space().grid()[current_coord].remove_creature(creature)
            new_cell = self.space().grid()[current_coord - 1].insert_creature(creature)
            creature.update_cell(new_cell)

    def creature_mate(self, creature):
        self.statistics.action_dist[Actions.get_available_action_indx(Actions.MATE)] += 1
        if creature.age() < Config.ConfigBiology.MATURITY_AGE:
            if creature.energy() < Config.ConfigBiology.MOVE_ENERGY:
                self.kill_creature(creature)
                return
            creature.reduce_energy(Config.ConfigBiology.MOVE_ENERGY)
            return

        if creature.energy() < Config.ConfigBiology.MATE_ENERGY:
            self.kill_creature(creature)
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
        self.create_creature(new_dna, creature.coord(), parent=dominant_parent)

    def creature_divide(self, creature):
        self.statistics.action_dist[Actions.get_available_action_indx(Actions.DEVIDE)] += 1
        if creature.age() < Config.ConfigBiology.MATURITY_AGE and creature.energy()<30:
            if creature.energy() < Config.ConfigBiology.MOVE_ENERGY:
                self.kill_creature(creature)
                return
            creature.reduce_energy(Config.ConfigBiology.MOVE_ENERGY)
            return

        self.create_creature(dna=creature.dna(), coord=creature.coord(), energy=int(creature.energy() / 2), parent=creature)
        creature.reduce_energy(amount=int(creature.energy()/4))
        creature._age = 0

    def kill_creature(self, creature, cause='fatigue'):
        creature.reduce_energy(creature.energy())
        cell = creature.cell()
        creature.update_cell(None)
        cell.remove_creature(creature)
        if self.statistics is not None:
            if cause == 'fight':
                self.statistics.death_cause[1] += 1
            elif cause == 'elderly':
                self.statistics.death_cause[2] += 1
            else:
                self.statistics.death_cause[0] += 1

    def creature_fight(self, creature):
        self.statistics.action_dist[Actions.get_available_action_indx(Actions.FIGHT)] += 1
        if creature.energy() < Config.ConfigBiology.FIGHT_ENERGY:
            self.kill_creature(creature, 'fight')
            return
        creature.reduce_energy(Config.ConfigBiology.FIGHT_ENERGY)

        opponent = creature.cell().find_nearby_creature(creature)
        if opponent is None:
            return
        fight_res = utils.roll_fight(creature.energy(), opponent.energy())
        if fight_res == -1:
            energy_trans = int(opponent.energy() / 2)
            creature.add_energy(energy_trans)
            opponent.reduce_energy(energy_trans)
        else:
            energy_trans = int(creature.energy() / 2)
            opponent.add_energy(energy_trans)
            creature.reduce_energy(energy_trans)

    def creature_work(self, creature):
        self.statistics.action_dist[Actions.get_available_action_indx(Actions.WORK)] += 1
        if creature.energy() < Config.ConfigBiology.WORK_ENERGY:
            self.kill_creature(creature, 'work')
            return
        creature.reduce_energy(Config.ConfigBiology.WORK_ENERGY)
        creature.cell().add_food(Config.ConfigBiology.MEAL_SIZE)

    @staticmethod
    def get_creatures_counter():
        return Creature.counter
