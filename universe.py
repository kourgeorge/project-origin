__author__ = 'gkour'

from space import Space
from evolution import Evolution
from config import Config
import numpy as np
import utils
from creature_actions import Actions


class Universe:

    def __init__(self, races, statistics=None):
        self._creature_counter = 0
        self._races = races
        self._space = Space(Config.ConfigPhysics.SPACE_SIZE)
        self._time = 0
        for race in races:
            fathers_locations_i = np.random.choice(Config.ConfigPhysics.SPACE_SIZE, Config.ConfigPhysics.NUM_FATHERS)
            fathers_locations_j = np.random.choice(Config.ConfigPhysics.SPACE_SIZE, Config.ConfigPhysics.NUM_FATHERS)
            for n in range(Config.ConfigPhysics.NUM_FATHERS):
                dna = Evolution.random_dna()
                self.create_creature(race, id=self.allocate_id(), dna=dna,
                                     coord=(fathers_locations_i[n], fathers_locations_j[n]),
                                     age=0, parent=None)

        self.give_food(Config.ConfigPhysics.INITIAL_FOOD_AMOUNT)
        self.statistics = statistics

    def allocate_id(self):
        self._creature_counter += 1
        return self._creature_counter

    def get_creatures_counter(self):
        return self._creature_counter

    def get_races(self):
        return self._races

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
                    creature.execute_action()
            return self._time
        else:
            return None

    def get_time(self):
        return self._time

    # Food Supply management
    def give_food(self, amount):
        food_cells_i = np.random.choice(Config.ConfigPhysics.SPACE_SIZE, amount)
        food_cells_j = np.random.choice(Config.ConfigPhysics.SPACE_SIZE, amount)
        for n in range(amount):
            self.space().add_food((food_cells_i[n], food_cells_j[n]), 1)

    # Creatures Control
    def create_creature(self, race, id, dna, coord, age=0, energy=Config.ConfigBiology.INITIAL_ENERGY, parent=None):
        descendant = race(universe=self, id=id, dna=dna, age=age, energy=energy, parent=parent,
                          model_path=Config.ConfigBrain.MODEL_PATH)
        cell = self.space().insert_creature(descendant, coord)
        descendant.update_cell(cell)

    def get_all_creatures(self):
        return self.space().get_all_creatures()

    def get_food_distribution(self):
        return self.space().get_food_distribution()

    def get_creatures_distribution(self):
        return self.space().get_creatures_distribution()

    def num_creatures(self):
        return len(self.get_all_creatures())

    def races_dist(self):
        dist = []
        for race in self._races:
            num_in_race = [creature for creature in self.get_all_creatures() if creature.get_race() == race]
            dist.extend([len(num_in_race)])
        return np.asarray(dist)

    def kill_creature(self, creature, cause='fatigue'):
        creature.dying()
        creature.reduce_energy(creature.energy())
        cell = creature.cell()
        creature.update_cell(None)
        cell.remove_creature(creature)
        if self.statistics is not None:
            if cause == 'fight':
                self.statistics.death_cause[1] += 1
            elif cause == 'elderly':
                self.statistics.death_cause[2] += 1
            elif cause == 'fall':
                self.statistics.death_cause[3] += 1
            else:
                self.statistics.death_cause[0] += 1

    ## Creature Actions
    def creature_eat(self, creature):
        self.statistics.action_dist[Actions.enum_to_index(Actions.EAT)] += 1
        if creature.energy() < Config.ConfigBiology.MOVE_ENERGY:
            self.kill_creature(creature)
            return
        creature.reduce_energy(Config.ConfigBiology.MOVE_ENERGY)
        available_food = creature.cell().get_food()
        meal = min(Config.ConfigBiology.MEAL_SIZE, available_food)
        creature.add_energy(meal)
        creature.cell().remove_food(meal)

    def creature_move_left(self, creature):
        self.statistics.action_dist[Actions.enum_to_index(Actions.LEFT)] += 1
        self.move_creature(creature, Actions.LEFT)

    def creature_move_right(self, creature):
        self.statistics.action_dist[Actions.enum_to_index(Actions.RIGHT)] += 1
        self.move_creature(creature, Actions.RIGHT)

    def creature_move_up(self, creature):
        self.statistics.action_dist[Actions.enum_to_index(Actions.UP)] += 1
        self.move_creature(creature, Actions.UP)

    def creature_move_down(self, creature):
        self.statistics.action_dist[Actions.enum_to_index(Actions.DOWN)] += 1
        self.move_creature(creature, Actions.DOWN)

    def move_creature(self, creature, direction):
        if creature.energy() < Config.ConfigBiology.MOVE_ENERGY:
            self.kill_creature(creature)
            return
        creature.reduce_energy(Config.ConfigBiology.MOVE_ENERGY)

        i, j = creature.coord()
        if direction == Actions.RIGHT:
            rel_dim_coord = j
            if rel_dim_coord == Config.ConfigPhysics.SPACE_SIZE - 1:
                if not Config.ConfigPhysics.SLIPPERY_SPACE:
                    return
                self.kill_creature(creature, "fall")
                return
            self.space().remove_creature(creature)
            new_cell = self.space().insert_creature(creature, (i, j + 1))
            creature.update_cell(new_cell)

        if direction == Actions.LEFT:
            rel_dim_coord = j
            if rel_dim_coord == 0:
                if not Config.ConfigPhysics.SLIPPERY_SPACE:
                    return
                self.kill_creature(creature, "fall")
                return
            self.space().remove_creature(creature)
            new_cell = self.space().insert_creature(creature, (i, j - 1))
            creature.update_cell(new_cell)

        if direction == Actions.UP:
            rel_dim_coord = i
            if rel_dim_coord == 0:
                if not Config.ConfigPhysics.SLIPPERY_SPACE:
                    return
                self.kill_creature(creature, "fall")
                return
            self.space().remove_creature(creature)
            new_cell = self.space().insert_creature(creature, (i - 1, j))
            creature.update_cell(new_cell)

        if direction == Actions.DOWN:
            rel_dim_coord = i
            if rel_dim_coord == Config.ConfigPhysics.SPACE_SIZE - 1:
                if not Config.ConfigPhysics.SLIPPERY_SPACE:
                    return
                self.kill_creature(creature)
                return
            self.space().remove_creature(creature)
            new_cell = self.space().insert_creature(creature, (i + 1, j))
            creature.update_cell(new_cell)

    def creature_mate(self, creature):
        self.statistics.action_dist[Actions.enum_to_index(Actions.MATE)] += 1
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
        mate_body = creature.cell().find_nearby_creature_from_same_race(creature)
        if mate_body is None:
            return

        # Selecting the dominant parent, based on the energy level, to copy the wisdom from
        dominant_parent = creature
        if mate_body.energy() > creature.energy():
            dominant_parent = mate_body

        new_dna = Evolution.mix_dna(creature.dna(), mate_body.dna())
        self.create_creature(creature.get_race(), self.allocate_id(), new_dna, creature.coord(), parent=dominant_parent)

    def creature_divide(self, creature):
        self.statistics.action_dist[Actions.enum_to_index(Actions.DIVIDE)] += 1
        if creature.age() < Config.ConfigBiology.MATURITY_AGE or creature.energy() < 2 * Config.ConfigBiology.INITIAL_ENERGY:
            if creature.energy() < Config.ConfigBiology.MOVE_ENERGY:
                self.kill_creature(creature)
                return
            creature.reduce_energy(Config.ConfigBiology.MOVE_ENERGY)
            return

        self.create_creature(creature.get_race(), self.allocate_id(), dna=creature.dna(), coord=creature.coord(),
                             energy=int(creature.energy() / 2) + 1,
                             parent=creature)
        creature.reduce_energy(amount=int(creature.energy() / 2))
        creature._age = 1

    def creature_fight(self, creature):
        self.statistics.action_dist[Actions.enum_to_index(Actions.FIGHT)] += 1
        if creature.energy() < Config.ConfigBiology.FIGHT_ENERGY:
            self.kill_creature(creature, 'fight')
            return
        creature.reduce_energy(Config.ConfigBiology.FIGHT_ENERGY)

        opponent = creature.cell().find_nearby_creature_from_different_race(creature)
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
        self.statistics.action_dist[Actions.enum_to_index(Actions.WORK)] += 1
        if creature.energy() < Config.ConfigBiology.WORK_ENERGY:
            self.kill_creature(creature, 'work')
            return
        creature.reduce_energy(Config.ConfigBiology.WORK_ENERGY)
        creature.cell().add_food(Config.ConfigBiology.MEAL_SIZE)
