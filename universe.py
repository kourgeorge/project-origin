from space import Space
from creature import Creature
from evolution import Evolution
import numpy as np
import utils


class Universe:

    def __init__(self, num_fathers):
        self._mate_energy = Creature.INITIAL_ENERGY/4
        self._move_energy = 1
        self._fight_energy = 5
        self._space_size = 10
        self._space = Space(self._space_size)
        self__stats = {}

        locations = np.random.choice(self._space_size, num_fathers)

        for i in range(num_fathers):
            dna = utils.random_dna(Creature.DNA_SIZE)
            self.create_creature(dna, locations[i])

    def space(self):
        return self._space

    def feed(self, creature):
        available_food = creature.cell().get_food()
        creature.add_energy(available_food)
        creature.cell().remove_food(available_food)

    # def add_creature(self, location, creature):
    #     if self.is_legal_location(location):
    #         self.space().grid()[location].insert_creature(creature)
    #
    # def is_legal_location(self, location):
    #     return 0 < location < self._space_size

    def move_creature(self, creature, direction):
        if creature.energy() < self._mate_energy:
            self.kill(creature)
            return
        creature.reduce_energy(self._move_energy)

        current_coord = creature.coord()
        if direction == 1:
            if current_coord == self._space_size - 1:
                return
            self.space().grid()[current_coord].remove_creature(creature)
            self.space().grid()[current_coord + 1].insert_creature(creature)
        if direction == -1:
            if current_coord == 0:
                return
            self.space().grid()[current_coord].remove_creature(creature)
            self.space().grid()[current_coord - 1].insert_creature(creature)

        creature.reduce_energy(self._move_energy)

    def mate_creature(self, creature):

        if creature.energy() < self._mate_energy:
            self.kill(creature)
            return
        creature.reduce_energy(self._mate_energy)
        mate_body = creature.cell().get_mate_body(creature)
        if mate_body is None:
            return
        new_dna = Evolution.mix_dna(creature.dna(), mate_body.dna())
        self.create_creature(new_dna, creature.coord())

    def kill(self, creature):
        cell = creature.cell()
        cell.remove_creature(creature)

    def fight(self, creature):
        if creature.energy() < self._fight_energy:
            self.kill(creature)
            return
        opponent = creature.cell().get_mate_body(creature)
        if opponent is None:
            return
        creature.reduce_energy(self._fight_energy)
        fight_res = utils.roll_fight(creature.energy(), opponent.energy())
        if fight_res > 0:
            opponent.add_energy(creature.energy())
            #opponent.add_energy(5)
            self.kill(creature)
        else:
            creature.add_energy(opponent.energy())
            #creature.add_energy(5)
            self.kill(opponent)


    def get_state_in_coord(self, coord):
        return self.space().get_state_in_coord(coord)

    def create_creature(self, dna, coord):
        descendant = Creature(universe=self, dna=dna, id=Creature.allocate_id())
        self.space().grid()[coord].insert_creature(descendant)

    def pass_time(self):
        for cell in self.space().grid():
            for creature in cell.creatures():
                creature.act()

    def give_food(self):
        num_iterations = 1
        food_cells = np.random.choice(self._space_size, num_iterations)
        for i in range(num_iterations):
            self.space().grid()[food_cells[i]].add_food(1)

    def get_all_creatures(self):
        return self.space().get_all_creatures()

