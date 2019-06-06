__author__ = 'gkour'

from cell import Cell
import numpy as np
from itertools import chain


class Space:
    def __init__(self, space_size):
        self._space_size = space_size
        self._grid = []
        for i in range(space_size):
            self._grid = [[Cell((i, j)) for j in range(self._space_size)] for i in range(self._space_size)]

    def grid(self):
        return self._grid

    def cells(self):
        return list(chain.from_iterable(self._grid))

    def update_sounds(self, time):
        for cell in self.cells():
            cell.remove_sounds(time)

    def insert_creature(self, creature, coord):
        if not self.valid_coord(coord):
            print("Exception: bad coordinated in space.insert_creature")
            return None
        cell = self._grid[coord[0]][coord[1]]
        cell.insert_creature(creature)
        return cell

    def add_food(self, coord, amount):
        if not self.valid_coord(coord):
            print("Exception: bad coordinated in space.add_food")
            return None
        cell = self._grid[coord[0]][coord[1]]
        cell.add_food(amount)
        return cell

    def remove_creature(self, creature):
        x, y = creature.coord()
        self._grid[x][y].remove_creature(creature)

    def get_state_in_coord(self, coord, vision_range, races):
        if not self.valid_coord(coord):
            raise Exception("Exception: bad coordinated in space.get_state_in_coord")
        state_dim_size = 2 * vision_range + 1
        dims = len(races) + 2  # races, food, and sound
        state = np.ones([dims, state_dim_size, state_dim_size]) * -1

        for i in range(state_dim_size):
            for j in range(state_dim_size):
                abs_i = coord[0] - vision_range + i
                abs_j = coord[1] - vision_range + j
                if 0 <= abs_i < self._space_size and 0 <= abs_j < self._space_size:
                    state[:, i, j] = self._grid[abs_i][abs_j].get_state_in_cell(races)
        return state

    def get_all_creatures(self):
        return [creature for cell in self.cells() for creature in cell.creatures()]

    def get_food_distribution(self):
        return [[self._grid[i][j].get_food() for j in range(self._space_size)] for i in range(self._space_size)]

    def get_creatures_distribution(self):
        return [[self._grid[i][j].num_creatures() for j in range(self._space_size)] for i in range(self._space_size)]

    def get_sounds_distribution(self):
        return [[len(self._grid[i][j].get_sounds()) for j in range(self._space_size)] for i in range(self._space_size)]

    def valid_coord(self, coord):
        x, y = coord
        return 0 <= x < self._space_size and 0 <= y < self._space_size

    def find_nearby_creature(self, creature):
        nearby_creatures = creature.cell().creatures()
        if len(nearby_creatures) < 2:
            return None
        others = [creat for creat in nearby_creatures if creat != creature]
        return np.random.permutation(others)[0]

    def find_nearby_creature_from_same_race(self, creature):
        others = self.get_nearby_creatures_from_same_race(creature)
        if others:
            return np.random.permutation(others)[0]
        return None

    def find_nearby_creature_from_different_race(self, creature):
        others = self.get_nearby_creatures_from_different_race(creature)
        if others:
            return np.random.permutation(others)[0]
        return None

    def get_nearby_creatures_from_same_race(self, creature):
        return [creat for creat in creature.cell().creatures() if
                creat != creature and creat.race_name() == creature.race_name()]

    def get_nearby_creatures_from_different_race(self, creature):
        return [creat for creat in creature.cell().creatures() if creat.race_name() != creature.race_name()]

    def __str__(self):
        string = ''
        for cell in self._grid:
            string = string + str(cell) + ' '

        return string
