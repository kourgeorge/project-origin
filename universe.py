__author__ = 'gkour'

from space import Space
from evolution import Evolution
from config import ConfigPhysics, ConfigBiology, ConfigBrain
import numpy as np
import utils
from creature_actions import Actions
from sound import Sound


class Universe:

    def __init__(self, races, statistics=None):
        self._creature_counter = 0
        self._races = races
        self._space = Space(ConfigPhysics.SPACE_SIZE)
        self._time = 0
        self.statistics = statistics
        for race in races:
            num_fathers = ConfigPhysics.NUM_FATHERS

            fathers_locations_i = np.random.choice(ConfigPhysics.SPACE_SIZE, num_fathers)
            fathers_locations_j = np.random.choice(ConfigPhysics.SPACE_SIZE, num_fathers)
            ages = np.random.randint(low=0, high=ConfigBiology.BASE_LIFE_EXPECTANCY, size=num_fathers)
            for n in range(num_fathers):
                dna = Evolution.mutate_dna(race.race_basic_dna())

                self.create_creature(race, id=self.allocate_id(), dna=dna,
                                     coord=(fathers_locations_i[n], fathers_locations_j[n]),
                                     age=ages[n], parents=None)

        self.give_food(ConfigPhysics.INITIAL_FOOD_AMOUNT)

    def allocate_id(self):
        self._creature_counter += 1
        return self._creature_counter

    def get_creatures_counter(self):
        return self._creature_counter

    def get_races(self):
        return self._races

    def num_races(self):
        return len(self._races)

    # Space Management
    def space(self):
        return self._space

    def get_surroundings(self, coord, vision_range):
        return self._space.get_state_in_coord(coord, vision_range, self._races)

    # Time Management
    def pass_time(self):
        self._time += 1

        num_creatures = self.num_creatures()
        if self._time < ConfigPhysics.ETERNITY and num_creatures > 0:
            self.give_food(round(num_creatures * ConfigPhysics.FOOD_CREATURE_RATIO))
            for creature in self.get_all_creatures():
                if creature.alive():
                    self.execute_action(creature)
            self.space().update_sounds(self._time)
            return self.num_creatures()
        else:
            return None

    def get_time(self):
        return self._time

    # Food Supply management
    def give_food(self, amount):
        food_cells_i = np.random.choice(ConfigPhysics.SPACE_SIZE, amount)
        food_cells_j = np.random.choice(ConfigPhysics.SPACE_SIZE, amount)
        for n in range(amount):
            self.space().add_food((food_cells_i[n], food_cells_j[n]), 1)

    # Creatures Control
    def create_creature(self, race, id, dna, coord, age=0, energy=ConfigBiology.INITIAL_ENERGY, parents=None):
        descendant = race(universe=self, id=id, dna=dna, age=age, energy=energy, parents=parents)
        cell = self.space().insert_creature(descendant, coord)
        descendant.update_cell(cell)

    def get_all_creatures(self):
        return np.random.permutation(self.space().get_all_creatures()).tolist()

    def get_food_distribution(self):
        return self.space().get_food_distribution()

    def get_creatures_distribution(self):
        return self.space().get_creatures_distribution()

    def num_creatures(self):
        return len(self.get_all_creatures())

    def execute_action(self, creature):
        if creature.age() > creature.life_expectancy():
            self.kill_creature(creature, cause='elderly')
            return
        creature.increase_age()
        previous_energy = creature.energy()
        state = creature.get_state()
        decision = creature.decide(state)
        action = creature.index_to_enum(decision)
        self.statistics.action_dist.append([creature.id(), creature.get_race(), Actions.enum_to_index(action)])
        if action == Actions.LEFT:
            self.creature_move_left(creature)
        if action == Actions.RIGHT:
            self.creature_move_right(creature)
        if action == Actions.UP:
            self.creature_move_up(creature)
        if action == Actions.DOWN:
            self.creature_move_down(creature)
        if action == Actions.EAT:
            self.creature_eat(creature)
        if action == Actions.MATE:
            self.creature_mate(creature)
        if action == Actions.FIGHT:
            self.creature_fight(creature)
        if action == Actions.WORK:
            self.creature_work(creature)
        if action == Actions.DIVIDE:
            self.creature_divide(creature)
        if action == Actions.VOCALIZE:
            self.creature_vocalize(creature)

        dec_1hot = np.zeros(creature.num_actions())
        dec_1hot[decision] = 1
        reward = creature.energy() - previous_energy
        new_state = creature.get_state() if creature.alive() else creature.dead_state()
        terminated = False if creature.alive() else True
        creature.add_experience([state, dec_1hot, reward, new_state, terminated])

        if creature.age() % creature.learning_frequency() == 0:
            creature.smarten()

    def races_dist(self):
        dist = []
        for race in self.get_races():
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
                self.statistics.death_cause.append([creature.id(), creature.get_race(), 1])
            elif cause == 'elderly':
                self.statistics.death_cause.append([creature.id(), creature.get_race(), 2])
            elif cause == 'fall':
                self.statistics.death_cause.append([creature.id(), creature.get_race(), 3])
            else:  # fatigue
                self.statistics.death_cause.append([creature.id(), creature.get_race(), 0])
            print(self.statistics.death_cause[-1])

    ## AbstractCreature Actions
    def creature_eat(self, creature):
        if creature.energy() < ConfigBiology.MOVE_ENERGY:
            self.kill_creature(creature)
            return
        creature.reduce_energy(ConfigBiology.MOVE_ENERGY)
        available_food = creature.cell().get_food()
        meal = min(ConfigBiology.MEAL_SIZE, available_food)
        creature.add_energy(meal)
        creature.cell().remove_food(meal)

    def creature_move_left(self, creature):
        self.move_creature(creature, Actions.LEFT)

    def creature_move_right(self, creature):
        self.move_creature(creature, Actions.RIGHT)

    def creature_move_up(self, creature):
        self.move_creature(creature, Actions.UP)

    def creature_move_down(self, creature):
        self.move_creature(creature, Actions.DOWN)

    def move_creature(self, creature, direction):
        if creature.energy() < ConfigBiology.MOVE_ENERGY:
            self.kill_creature(creature)
            return
        creature.reduce_energy(ConfigBiology.MOVE_ENERGY)

        i, j = creature.coord()
        if direction == Actions.RIGHT:
            rel_dim_coord = j
            if rel_dim_coord == ConfigPhysics.SPACE_SIZE - 1:
                if not ConfigPhysics.SLIPPERY_SPACE:
                    return
                self.kill_creature(creature, "fall")
                return
            self.space().remove_creature(creature)
            new_cell = self.space().insert_creature(creature, (i, j + 1))
            creature.update_cell(new_cell)

        if direction == Actions.LEFT:
            rel_dim_coord = j
            if rel_dim_coord == 0:
                if not ConfigPhysics.SLIPPERY_SPACE:
                    return
                self.kill_creature(creature, "fall")
                return
            self.space().remove_creature(creature)
            new_cell = self.space().insert_creature(creature, (i, j - 1))
            creature.update_cell(new_cell)

        if direction == Actions.UP:
            rel_dim_coord = i
            if rel_dim_coord == 0:
                if not ConfigPhysics.SLIPPERY_SPACE:
                    return
                self.kill_creature(creature, "fall")
                return
            self.space().remove_creature(creature)
            new_cell = self.space().insert_creature(creature, (i - 1, j))
            creature.update_cell(new_cell)

        if direction == Actions.DOWN:
            rel_dim_coord = i
            if rel_dim_coord == ConfigPhysics.SPACE_SIZE - 1:
                if not ConfigPhysics.SLIPPERY_SPACE:
                    return

                self.kill_creature(creature, "fall")
                return
            self.space().remove_creature(creature)
            new_cell = self.space().insert_creature(creature, (i + 1, j))
            creature.update_cell(new_cell)

    def creature_mate(self, creature):
        if creature.age() < ConfigBiology.MATURITY_AGE:
            if creature.energy() < ConfigBiology.MOVE_ENERGY:
                self.kill_creature(creature)
                return
            creature.reduce_energy(ConfigBiology.MOVE_ENERGY)
            return

        if creature.energy() < ConfigBiology.MATE_ENERGY:
            self.kill_creature(creature)
            return

        creature.reduce_energy(ConfigBiology.MATE_ENERGY)
        potential_spouses = self.space().get_nearby_creatures_from_same_race(creature)
        spouse = creature.select_spouse(potential_spouses)
        if spouse is None:
            return
        new_dna = Evolution.mix_dna(creature.dna(), spouse.dna())
        self.create_creature(creature.get_race(), self.allocate_id(), new_dna, creature.coord(),
                             parents=[creature, spouse])

    def creature_divide(self, creature):
        if creature.age() < ConfigBiology.MATURITY_AGE:
            if creature.energy() < ConfigBiology.MOVE_ENERGY:
                self.kill_creature(creature)
                return
            creature.reduce_energy(ConfigBiology.MOVE_ENERGY)
            return

        self.create_creature(creature.get_race(), self.allocate_id(), dna=Evolution.mutate_dna(creature.dna()),
                             coord=creature.coord(),
                             energy=int(creature.energy() / 2) + 1,
                             parents=[creature])
        creature.reduce_energy(amount=int(creature.energy() / 2))
        creature._age = 1

    def creature_fight(self, creature):
        if creature.energy() < ConfigBiology.FIGHT_ENERGY:
            self.kill_creature(creature, 'fight')
            return
        creature.reduce_energy(ConfigBiology.FIGHT_ENERGY)

        if creature.self_race_enemy():
            opponent = self.space().find_nearby_creature(creature)
        else:
            opponent = self.space().find_nearby_creature_from_different_race(creature)
        if opponent is None:
            return

        opponent_support = creature.cell().race_energy_level(opponent.get_race()) - opponent.energy()
        creature_support = creature.cell().race_energy_level(creature.get_race()) - creature.energy()

        fight_res = utils.roll_fight(creature.energy() + creature_support, opponent.energy() + opponent_support)

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
        if creature.energy() < ConfigBiology.WORK_ENERGY:
            self.kill_creature(creature, 'work')
            return
        creature.reduce_energy(ConfigBiology.WORK_ENERGY)
        creature.cell().add_food(ConfigBiology.MEAL_SIZE)


    def creature_vocalize(self, creature):
        self.statistics.action_dist[Actions.enum_to_index(Actions.VOCALIZE)] += 1
        if creature.energy() < ConfigBiology.VOCALIZE_ENERGY:
            self.kill_creature(creature, 'vocalize')
            return
        if [s for s in creature.cell().get_sounds() if s.creature() != creature]:
            creature.add_energy(2)
        creature.reduce_energy(ConfigBiology.VOCALIZE_ENERGY)
        creature.cell().add_sound(Sound(creature, self._time))
